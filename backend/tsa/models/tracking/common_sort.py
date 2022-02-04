from abc import ABC
from typing import List, Tuple

import numpy as np

from tsa.models import TrackableModel
from tsa.typing import MATCHED_BBOXES, MATCHED_IDS

from .tracker import Tracker


class CommonSORT(ABC, TrackableModel):
    current_trackers: List[Tracker]

    def _matched_trackers(self, matches, detections) -> Tuple[MATCHED_BBOXES, MATCHED_IDS]:
        """Match states with proper detections at proper positions."""
        matched_boxes, matched_ids = np.ma.masked_all(detections.shape, dtype=np.float32), [None] * detections.shape[0]

        for tracker_position, detection_position in matches:
            tracker, detection = self.current_trackers[tracker_position], detections[detection_position]

            if tracker.is_active:
                matched_boxes[detection_position] = tracker.state
                matched_ids[detection_position] = tracker.id

        return matched_boxes, matched_ids

    def _unmatched_trackers(self, unmatched_trackers) -> Tuple[MATCHED_BBOXES, MATCHED_IDS, int]:
        """Use existing trackers to predict next detections for vehicles that were missed by the detection model."""
        unmatched_boxes, unmatched_ids, new_number_of_boxes = [], [], 0

        for tracker_position in unmatched_trackers:
            tracker = self.current_trackers[tracker_position]

            if tracker.is_active:
                new_number_of_boxes += 1
                unmatched_boxes.append(tracker.state)
                unmatched_ids.append(tracker.id)

        return np.reshape(np.asarray(unmatched_boxes), (-1, 4)), unmatched_ids, new_number_of_boxes
