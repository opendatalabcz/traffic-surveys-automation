"""Implementation of DeepSORT in our system.

It uses the raw code implemented by the authors of the paper in package `deep_sort_raw`.

Code in this module is inspired by
https://github.com/levan92/deep_sort_realtime/tree/fb4cf8e32cca33a2dab127d4d6e265adfb190e88
which creates a wrapper around the original Deep SORT but uses pytorch which is not suitable for us.
"""
from typing import Tuple

import numpy as np
import tensorflow as tf

from tsa.models.tracking.common_sort import CommonSORT
from tsa.typing import MATCHED_IDS, NP_ARRAY

from .deep_sort_raw import nn_matching
from .deep_sort_raw.detection import Detection
from .deep_sort_raw.tracker import Tracker
from .embedder import embedding_model
from .preprocessor import frame_detections_to_crops


class DeepSORT(CommonSORT):
    def __init__(
        self, min_updates: int, max_age: int, iou_threshold: float, max_cosine_distance: float, nn_budget: int
    ):
        self.tracker = Tracker(
            nn_matching.NearestNeighborDistanceMetric(max_cosine_distance, nn_budget),
            iou_threshold,
            max_age,
            min_updates,
        )
        self.current_trackers = self.tracker.tracks  # copies reference to the same list of tracks
        self.embedder = embedding_model()

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

        matched_boxes, matched_ids = self._matched_trackers(matched, detections)
        unmatched_boxes, unmatched_ids, new_boxes = self._unmatched_trackers(unmatched_trackers)

        self.tracker.update(matched, unmatched_trackers, unmatched_detections, detections_with_embeddings)

        return np.ma.concatenate((matched_boxes, unmatched_boxes), axis=0), matched_ids + unmatched_ids, new_boxes

    @tf.function
    def _generate_embeddings(self, frames, detections):
        crops = self.crop_bounding_boxes(frames, detections)
        crops = tf.cast(crops, tf.float32)
        merged_crops, batch_row_lengths = crops.merge_dims(0, 1), crops.row_lengths(axis=1)

        embeddings = self.embedder(merged_crops)
        embeddings = tf.RaggedTensor.from_row_lengths(embeddings, batch_row_lengths)
        embeddings = tf.where(tf.math.is_nan(embeddings), tf.zeros_like(embeddings), embeddings)
        return embeddings

    @staticmethod
    def crop_bounding_boxes(frames, raw_detections) -> tf.RaggedTensor:
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

        return frame_detections_to_crops(frames, detections)
