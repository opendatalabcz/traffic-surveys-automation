"""Implementation of DeepSORT in our system.

It uses the raw code implemented by the authors of the paper in package `deep_sort_raw`.

Code in this module is inspired by
https://github.com/levan92/deep_sort_realtime/tree/fb4cf8e32cca33a2dab127d4d6e265adfb190e88
which creates a wrapper around the original Deep SORT but uses pytorch which is not suitable for us.
"""
from typing import Tuple

import numpy as np
import tensorflow as tf

from tsa.models import TrackableModel
from tsa.logging import log
from tsa.typing import MATCHED_BBOXES, MATCHED_IDS, NP_ARRAY, NP_FRAME

from .deep_sort_raw import nn_matching
from .deep_sort_raw.detection import Detection
from .deep_sort_raw.tracker import Tracker
from .embedder import mobilenet_embedder


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
        self.embedder = mobilenet_embedder()

    def track(self, detections, **kwargs):
        embeddings = self._generate_embeddings(kwargs.pop("frames"), detections)

        for single_detections, single_embeddings in zip(detections, embeddings):
            yield self._track_single_frame(single_detections, single_embeddings)

    def _track_single_frame(self, detections, embeddings) -> Tuple[NP_ARRAY, MATCHED_IDS, int]:
        detections_with_embeddings = [
            Detection(detection, embedding) for detection, embedding in zip(detections, embeddings)
        ]

        self.tracker.predict()
        matched, unmatched_trackers, unmatched_detections = self.tracker.match(detections_with_embeddings)

        boxes, ids = self._match_existing_trackers(matched, detections)
        boxes, ids, new_boxes = self._add_unmatched_trackers(unmatched_trackers, boxes, ids)

        self.tracker.update(matched, unmatched_trackers, unmatched_detections, detections_with_embeddings)

        return np.array(boxes, dtype=object), ids, new_boxes

    @tf.function
    def _generate_embeddings(self, frames, detections):
        crops = self.crop_bounding_boxes(frames, detections)
        crops = tf.cast(crops, tf.float32)
        merged_crops, batch_row_lengths = crops.merge_dims(0, 1), crops.row_lengths(axis=1)

        embeddings = self.embedder(merged_crops)
        embeddings = tf.RaggedTensor.from_row_lengths(embeddings, batch_row_lengths)
        embeddings = tf.where(tf.math.is_nan(embeddings), tf.zeros_like(embeddings), embeddings)
        return embeddings

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
    def crop_bounding_boxes(frames, raw_detections) -> tf.RaggedTensor:
        def frame_to_boxes(input_data):
            frame, frame_detections = input_data
            return tf.map_fn(
                lambda bbox: tf.RaggedTensor.from_tensor(frame[bbox[1] : bbox[3], bbox[0] : bbox[2]]),
                frame_detections,
                infer_shape=False,
                fn_output_signature=tf.RaggedTensorSpec((None, None, 3), dtype=tf.uint8, ragged_rank=1),
            )

        detections = tf.cast(raw_detections, tf.int32)
        detections = tf.stack(
            (
                tf.math.maximum(0, detections[:, :, 0]),
                tf.math.maximum(0, detections[:, :, 1]),
                tf.math.minimum(tf.shape(frames)[2], detections[:, :, 2]),
                tf.math.minimum(tf.shape(frames)[1], detections[:, :, 3]),
            ),
            axis=2,
        )

        return tf.map_fn(
            frame_to_boxes,
            (frames, detections),
            fn_output_signature=tf.RaggedTensorSpec((None, None, None, 3), dtype=tf.uint8, ragged_rank=2),
        )
