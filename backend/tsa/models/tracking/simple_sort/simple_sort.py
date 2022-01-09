"""Simple online and realtime tracking implementation.

This follows the algorithm described in Bewley A. et al.: Simple Online and Realtime Tracking.
DOI: 10.1109/ICIP.2016.7533003.
GitHub repository: https://github.com/abewley/sort/tree/bce9f0d1fc8fb5f45bf7084130248561a3d42f31.
"""
from typing import List, Optional, Tuple

import numpy as np

from tsa import bbox, typing
from tsa.models import TrackableModel

from .association import associate_detections_to_trackers
from .tracker import Tracker

MATCHED_BBOXES = List[Optional[typing.NP_ARRAY]]
MATCHED_IDS = List[Optional[str]]


class SimpleSORT(TrackableModel):
    def __init__(self, min_updates: int, max_age: int, iou_threshold: float):
        # init configurable algorithm variables
        self.iou_threshold = iou_threshold
        self.tracker_config = {"min_updates": min_updates, "max_age": max_age}
        # prepare a list for storing active trackers
        self.active_trackers: List[Tracker] = []

    def track(self, detections: List[bbox.BBox]) -> Tuple[typing.NP_ARRAY, MATCHED_IDS, int]:
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
            if self.active_trackers[i].is_deleted:
                self.active_trackers.pop(i)

        # create new trackers
        for i in unmatched_detections:
            new_tracker = Tracker(numpy_detections[i], **self.tracker_config)
            self.active_trackers.append(new_tracker)

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

            if tracker.is_active:
                matched_boxes[detection_position] = tracker.state
                matched_ids[detection_position] = tracker.id

        return matched_boxes, matched_ids

    def _add_unmatched_trackers(self, unmatched_trackers, boxes, ids) -> Tuple[MATCHED_BBOXES, MATCHED_IDS, int]:
        """Use existing trackers to predict next detections for vehicles that were missed by the detection model."""
        new_number_of_boxes = 0

        for tracker_position in unmatched_trackers:
            tracker = self.active_trackers[tracker_position]

            if tracker.is_active:
                new_number_of_boxes += 1
                boxes.append(tracker.state)
                ids.append(tracker.id)

        return boxes, ids, new_number_of_boxes
