"""Implementation of DeepSORT in our system.

It uses the raw code implemented by the authors of the paper in package `deep_sort_raw`.

Code in this module is inspired by
https://github.com/levan92/deep_sort_realtime/tree/fb4cf8e32cca33a2dab127d4d6e265adfb190e88
which creates a wrapper around the original Deep SORT but uses pytorch which is not suitable for us.
"""
from typing import List, Tuple

import numpy as np

from tsa.bbox import BBox
from tsa.models import TrackableModel
from tsa.typing import MATCHED_BBOXES, MATCHED_IDS, NP_ARRAY, NP_FRAME

from .deep_sort_raw import nn_matching
from .deep_sort_raw.detection import Detection
from .deep_sort_raw.tracker import Tracker
from .embedder import MobileNetEmbedder


class DeepSORT(TrackableModel):
    def __init__(
        self, min_updates: int, max_age: int, iou_threshold: float, max_cosine_distance: float, nn_budget: int
    ):
        self.tracker = Tracker(
            nn_matching.NearestNeighborDistanceMetric(max_cosine_distance, nn_budget),
            iou_threshold,
            max_age,
            min_updates,
        )
        self.embedder = MobileNetEmbedder()

    def track(self, detections: List[BBox], **kwargs) -> Tuple[NP_ARRAY, MATCHED_IDS, int]:
        numpy_detections = np.array([detection.to_rectangle() for detection in detections])

        embeddings = self._generate_embeddings(kwargs.pop("frame"), numpy_detections)
        detections_with_embeddings = [
            Detection(detection, embedding) for detection, embedding in zip(numpy_detections, embeddings)
        ]

        self.tracker.predict()
        matched, unmatched_trackers, unmatched_detections = self.tracker.match(detections_with_embeddings)

        boxes, ids = self._match_existing_trackers(matched, numpy_detections)
        boxes, ids, new_boxes = self._add_unmatched_trackers(unmatched_trackers, boxes, ids)

        self.tracker.update(matched, unmatched_trackers, unmatched_detections, detections_with_embeddings)

        return np.array(boxes, dtype=object), ids, new_boxes

    def _generate_embeddings(self, frame: NP_FRAME, detected_bboxes):
        assert frame is not None, "Embedding frame is missing in DeepSORT."

        frame_crops_by_bbox = self.crop_bb(frame, detected_bboxes)
        np_predictions = self.embedder.predict_on_batch(frame_crops_by_bbox)
        np_predictions = np.nan_to_num(np_predictions, copy=False, nan=0.0)
        return np_predictions

    def _match_existing_trackers(self, matches, detections) -> Tuple[MATCHED_BBOXES, MATCHED_IDS]:
        """Match states with proper detections at proper positions."""
        matched_boxes, matched_ids = [None] * detections.shape[0], [None] * detections.shape[0]

        for tracker_position, detection_position in matches:
            tracker, detection = self.tracker.tracks[tracker_position], detections[detection_position]

            if tracker.is_active:
                matched_boxes[detection_position] = tracker.state
                matched_ids[detection_position] = tracker.id

        return matched_boxes, matched_ids

    def _add_unmatched_trackers(self, unmatched_trackers, boxes, ids) -> Tuple[MATCHED_BBOXES, MATCHED_IDS, int]:
        """Use existing trackers to predict next detections for vehicles that were missed by the detection model."""
        new_number_of_boxes = 0

        for tracker_position in unmatched_trackers:
            tracker = self.tracker.tracks[tracker_position]

            if tracker.is_active:
                new_number_of_boxes += 1
                boxes.append(tracker.state)
                ids.append(tracker.id)

        return boxes, ids, new_number_of_boxes

    @staticmethod
    def crop_bb(frame, raw_detections):
        crops = []
        im_height, im_width = frame.shape[:2]
        for detection in raw_detections:
            l, t, r, b = detection.astype(np.int32)
            crop_l = max(0, l)
            crop_r = min(im_width, r)
            crop_t = max(0, t)
            crop_b = min(im_height, b)
            crops.append(frame[crop_t:crop_b, crop_l:crop_r])
        return crops
