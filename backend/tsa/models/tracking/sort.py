"""Simple online and realtime tracking implementation.

This follows the algorithm described in Bewley A. et al.: Simple Online and Realtime Tracking.
DOI: 10.1109/ICIP.2016.7533003.
GitHub repository: https://github.com/abewley/sort/tree/bce9f0d1fc8fb5f45bf7084130248561a3d42f31.
"""
from typing import List, Optional, Tuple

import numpy as np
from scipy.optimize import linear_sum_assignment

from tsa import typing
from tsa.bbox import BBox
from tsa.cv2.kalman_filter import KalmanFilter
from tsa.models import TrackableModel

MATCHED_BBOXES = List[Optional[typing.NP_ARRAY]]
MATCHED_IDS = List[Optional[str]]


def iou_batch(bb_test, bb_gt):
    """Compute an intersection over union on a batch of bounding boxes.

    Adopted from https://github.com/abewley/sort/blob/bce9f0d1fc8fb5f45bf7084130248561a3d42f31/sort.py#L47.
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


def associate_detections_to_trackers(detections, trackers, iou_threshold: float):
    """Assigns detections to tracked object, both represented as bounding boxes.

    Returns 3 lists of matches, unmatched_detections and unmatched_trackers.
    Adopted from https://github.com/abewley/sort/blob/bce9f0d1fc8fb5f45bf7084130248561a3d42f31/sort.py#L154.
    """
    if len(trackers) == 0:
        return np.empty((0, 2), dtype=int), np.arange(len(detections)), np.empty((0, 5), dtype=int)

    if len(detections) == 0:
        return np.empty((0, 2), dtype=int), np.empty((0, 5), dtype=int), np.arange(len(trackers))

    iou_matrix = iou_batch(detections, trackers)

    if min(iou_matrix.shape) > 0:
        a = (iou_matrix > iou_threshold).astype(np.int32)
        if a.sum(1).max() == 1 and a.sum(0).max() == 1:
            matched_indices = np.stack(np.where(a), axis=1)
        else:
            row_indices, col_indices = linear_sum_assignment(-iou_matrix)
            matched_indices = np.array(list(zip(row_indices, col_indices)))
    else:
        matched_indices = np.empty(shape=(0, 2))

    unmatched_detections = [d for d, det in enumerate(detections) if d not in matched_indices[:, 0]]

    unmatched_trackers = [t for t, trk in enumerate(trackers) if t not in matched_indices[:, 1]]

    # filter out matched with low IOU, move them to unmatched detections and trackers
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
    def __init__(self, min_hits: int, max_age: int, iou_threshold: float):
        # init configurable algorithm variables
        self.min_hits, self.max_age, self.iou_threshold = min_hits, max_age, iou_threshold
        # prepare a list for storing active trackers
        self.active_trackers: List[KalmanFilter] = []

    def track(self, detections: List[BBox]) -> Tuple[typing.NP_ARRAY, MATCHED_IDS, int]:
        # convert input detection bboxes to a numpy array
        numpy_detections = np.array([detection.to_rectangle() for detection in detections])
        # get next bbox predictions from the existing trackers
        predictions = self._predict_active_trackers()
        # match predictions with detections
        matched, unmatched_detections, unmatched_trackers = associate_detections_to_trackers(
            numpy_detections, predictions, iou_threshold=self.iou_threshold
        )
        boxes, ids = self._update_and_match_existing_trackers(matched, numpy_detections)
        boxes, ids, new_boxes = self._add_unmatched_trackers(unmatched_trackers, boxes, ids)
        # delete old trackers
        for i in reversed(range(len(self.active_trackers))):
            if self.active_trackers[i].age > self.max_age:
                self.active_trackers.pop(i)
        # create new trackers
        for i in unmatched_detections:
            self.active_trackers.append(KalmanFilter(numpy_detections[i]))
        return np.array(boxes, dtype=object), ids, new_boxes

    def _predict_active_trackers(self):
        predictions = np.array([tracker.predict() for tracker in self.active_trackers])
        if predictions.size > 0:
            predictions = np.ma.compress_rows(np.ma.masked_invalid(predictions))
        return predictions

    def _update_and_match_existing_trackers(self, matches, detections) -> Tuple[MATCHED_BBOXES, MATCHED_IDS]:
        """Update the existing Kalman trackers, match them with proper detection positions."""
        matched_boxes, matched_ids = [None] * detections.shape[0], [None] * detections.shape[0]

        for detection_position, tracker_position in matches:
            tracker, detection = self.active_trackers[tracker_position], detections[detection_position]

            tracker.update(detection)

            if self._is_tracker_active(tracker):
                matched_boxes[detection_position] = tracker.state
                matched_ids[detection_position] = tracker.id

        return matched_boxes, matched_ids

    def _add_unmatched_trackers(self, unmatched_trackers, boxes, ids) -> Tuple[MATCHED_BBOXES, MATCHED_IDS, int]:
        """Use existing trackers to predict next detections for vehicles that were missed by the detection model."""
        new_number_of_boxes = 0

        for tracker_position in unmatched_trackers:
            tracker = self.active_trackers[tracker_position]

            if self._is_tracker_active(tracker):
                new_number_of_boxes += 1
                boxes.append(tracker.state)
                ids.append(tracker.id)

        return boxes, ids, new_number_of_boxes

    def _is_tracker_active(self, tracker: KalmanFilter) -> bool:
        return tracker.hits >= self.min_hits and tracker.age <= self.max_age
