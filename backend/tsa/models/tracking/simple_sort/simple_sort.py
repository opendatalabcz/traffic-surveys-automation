"""Simple online and realtime tracking implementation.

This follows the algorithm described in Bewley A. et al.: Simple Online and Realtime Tracking.
DOI: 10.1109/ICIP.2016.7533003.
GitHub repository: https://github.com/abewley/sort/tree/bce9f0d1fc8fb5f45bf7084130248561a3d42f31.
"""
from typing import List, Tuple

import numpy as np

from tsa.models.tracking.tracker import Tracker
from tsa.typing import MATCHED_IDS, NP_ARRAY

from ..common_sort import CommonSORT
from .association import associate_detections_to_trackers


class SimpleSORT(CommonSORT):
    def __init__(self, min_updates: int, max_age: int, iou_threshold: float):
        # init configurable algorithm variables
        self.iou_threshold = iou_threshold
        self.tracker_config = {"min_updates": min_updates, "max_age": max_age}
        # prepare a list for storing active trackers
        self.current_trackers: List[Tracker] = []

    def track(self, detections, **kwargs):
        for single_detections in detections:
            yield self._track_single_frame(single_detections)

    def _track_single_frame(self, detections) -> Tuple[NP_ARRAY, MATCHED_IDS, int]:
        # get next bbox predictions from the existing trackers
        predictions = self._predict_active_trackers()

        # match predictions with detections
        matched, unmatched_detections, unmatched_trackers = associate_detections_to_trackers(
            detections, predictions, iou_threshold=self.iou_threshold
        )

        matched_boxes, matched_ids = self._matched_trackers(matched, detections)
        unmatched_boxes, unmatched_ids, new_boxes = self._unmatched_trackers(unmatched_trackers)

        self._update_existing_trackers(matched, detections)

        for tracker_position in unmatched_trackers:
            self.current_trackers[tracker_position].mark_missed()

        self._delete_old_trackers()

        self._create_new_trackers(unmatched_detections, detections)

        return np.ma.concatenate((matched_boxes, unmatched_boxes), axis=0), matched_ids + unmatched_ids, new_boxes

    def _create_new_trackers(self, unmatched_detections, detections):
        for i in unmatched_detections:
            new_tracker = Tracker(detections[i], **self.tracker_config)
            self.current_trackers.append(new_tracker)

    def _delete_old_trackers(self):
        self.current_trackers = [tracker for tracker in self.current_trackers if not tracker.is_deleted]

    def _predict_active_trackers(self):
        predictions = np.array([tracker.predict() for tracker in self.current_trackers])
        if predictions.size > 0:
            predictions = np.ma.compress_rows(np.ma.masked_invalid(predictions))
        return predictions

    def _update_existing_trackers(self, matches, detections):
        for tracker_position, detection_position in matches:
            tracker, detection = self.current_trackers[tracker_position], detections[detection_position]

            tracker.update(detection)
