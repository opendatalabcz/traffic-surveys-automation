"""Simple online and realtime tracking model implementation.

The code is inspired by https://github.com/abewley/sort.
"""
from typing import List

import numpy as np
from scipy.optimize import linear_sum_assignment

from tsa.bbox import BBox
from tsa.cv2.kalman_tracker import KalmanTracker
from tsa.models import TrackableModel


def linear_assignment(cost_matrix):
    x, y = linear_sum_assignment(cost_matrix)
    return np.array(list(zip(x, y)))


def iou_batch(bb_test, bb_gt):
    """
    From SORT: Computes IOU between two bboxes in the form [x1,y1,x2,y2]
    """
    bb_gt = np.expand_dims(bb_gt, 0)
    bb_test = np.expand_dims(bb_test, 1)

    xx1 = np.maximum(bb_test[..., 0], bb_gt[..., 0])
    yy1 = np.maximum(bb_test[..., 1], bb_gt[..., 1])
    xx2 = np.minimum(bb_test[..., 2], bb_gt[..., 2])
    yy2 = np.minimum(bb_test[..., 3], bb_gt[..., 3])
    w = np.maximum(0.0, xx2 - xx1)
    h = np.maximum(0.0, yy2 - yy1)
    wh = w * h
    o = wh / (
        (bb_test[..., 2] - bb_test[..., 0]) * (bb_test[..., 3] - bb_test[..., 1])
        + (bb_gt[..., 2] - bb_gt[..., 0]) * (bb_gt[..., 3] - bb_gt[..., 1])
        - wh
    )
    return o


def associate_detections_to_trackers(detections, trackers, iou_threshold=0.3):
    """
    Assigns detections to tracked object (both represented as bounding boxes)
    Returns 3 lists of matches, unmatched_detections and unmatched_trackers
    """
    if len(trackers) == 0:
        return np.empty((0, 2), dtype=int), np.arange(len(detections)), np.empty((0, 5), dtype=int)

    iou_matrix = iou_batch(detections, trackers)

    if min(iou_matrix.shape) > 0:
        a = (iou_matrix > iou_threshold).astype(np.int32)
        if a.sum(1).max() == 1 and a.sum(0).max() == 1:
            matched_indices = np.stack(np.where(a), axis=1)
        else:
            matched_indices = linear_assignment(-iou_matrix)
    else:
        matched_indices = np.empty(shape=(0, 2))

    unmatched_detections = []
    for d, det in enumerate(detections):
        if d not in matched_indices[:, 0]:
            unmatched_detections.append(d)

    unmatched_trackers = []
    for t, trk in enumerate(trackers):
        if t not in matched_indices[:, 1]:
            unmatched_trackers.append(t)

    # filter out matched with low IOU
    matches = []
    for m in matched_indices:
        if iou_matrix[m[0], m[1]] < iou_threshold:
            unmatched_detections.append(m[0])
            unmatched_trackers.append(m[1])
        else:
            matches.append(m.reshape(1, 2))

    if len(matches) == 0:
        matches = np.empty((0, 2), dtype=int)
    else:
        matches = np.concatenate(matches, axis=0)

    return matches, np.array(unmatched_detections), np.array(unmatched_trackers)


class SORT(TrackableModel):
    min_hits = 1

    def __init__(self):
        self.frame_count = 0
        self.active_trackers: List[KalmanTracker] = []

    def track(self, detections: List[BBox]):
        self.frame_count += 1
        numpy_detections = np.array([detection.to_rectangle() for detection in detections])
        # get predictions from the existing trackers
        predictions = self._existing_trackers_predictions()
        # match predictions with detections
        matched, unmatched_detections, unmatched_trackers = associate_detections_to_trackers(
            numpy_detections, predictions
        )
        # update existing and matched trackers
        for m in matched:
            self.active_trackers[m[1]].update(numpy_detections[m[0]])
        # create new trackers
        for u in unmatched_detections:
            new_tracker = KalmanTracker(numpy_detections[u])
            self.active_trackers.append(new_tracker)
        # build and return final tracking
        return self._build_tracking()

    def _existing_trackers_predictions(self):
        predictions = np.array([tracker.predict() for tracker in self.active_trackers])
        if predictions.size > 0:
            predictions = np.ma.compress_rows(np.ma.masked_invalid(predictions))
        return predictions

    def _build_tracking(self):
        results_shapes, results_ids = [], []
        for tracker in self.active_trackers:
            if tracker.time_since_update < 1 and (
                tracker.hit_streak >= self.min_hits or self.frame_count <= self.min_hits
            ):
                results_shapes.append(tracker.state[:4].reshape((-1,)))
                results_ids.append(tracker.id)

        return np.array(results_shapes), results_ids
