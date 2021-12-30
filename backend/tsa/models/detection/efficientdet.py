from abc import ABC
from typing import Generator, Tuple, Any, List

import tensorflow as tf
import tensorflow_hub as tf_hub

from tsa.datasets import FramesDataset
from tsa.bbox import BBox
from tsa.logging import log
from tsa.models import PredictableModel


class EfficientDet(PredictableModel, ABC):
    models_dir = "/Users/ondrejpudis/traffic_survey_automation/models"
    model_path: str

    def __init__(self, max_outputs: int = 100, iou_threshold: float = 0.5, score_threshold: float = 0.5):
        super().__init__()
        self.batch_size = 8
        # define non-max-suppression config
        self.non_max_suppression_config = {
            "max_output_size_per_class": 20,
            "max_total_size": max_outputs,
            "iou_threshold": iou_threshold,
            "score_threshold": score_threshold,
            "clip_boxes": False,
        }
        # constant for filtering
        self.filtered_labels = tf.constant([2, 3, 4, 6, 8])
        self.tile_multiples = [1, 1, tf.shape(self.filtered_labels)[0]]

    def predict(self, dataset: FramesDataset) -> Generator:
        tf_dataset = dataset.as_tf_dataset(self.batch_size)

        for frames in tf_dataset:
            batch_bboxes, batch_classes, batch_scores = self._predict(frames)
            for frame, bboxes, classes, scores in zip(frames, batch_bboxes, batch_classes, batch_scores):
                yield frame.numpy(), BBox.from_tensor_list(bboxes, None, None), classes, scores

    def _build_model(self):
        saved_model = tf_hub.load(f"{self.models_dir}/{self.model_path}")
        return saved_model.signatures["serving_default"]

    @log()
    @tf.function()
    def _predict(self, frames):
        prediction = self.model(frames)
        bboxes, classes, scores = self._get(prediction)
        bboxes, classes, scores = self._filter(bboxes, classes, scores)
        bboxes, classes, scores = self._apply_non_max_suppression(bboxes, classes, scores)
        bboxes, classes, scores = self._cast(bboxes, classes, scores)
        return bboxes, classes, scores

    @staticmethod
    def _get(prediction):
        detections = prediction["detections:0"]
        bboxes = tf.stack(
            (detections[:, :, 1], detections[:, :, 2], detections[:, :, 3], detections[:, :, 4]),
            axis=2,
        )
        return bboxes, detections[:, :, 6], detections[:, :, 5]

    def _filter(self, bboxes, classes, scores):
        mask = tf.tile(tf.expand_dims(tf.cast(classes, tf.int32), -1), self.tile_multiples)
        mask = tf.reduce_any(tf.equal(mask, self.filtered_labels), -1)
        mask_function = tf.ragged.boolean_mask
        return mask_function(bboxes, mask), mask_function(classes, mask), mask_function(scores, mask)

    def _apply_non_max_suppression(self, bboxes, classes, scores):
        bboxes_tensor, bboxes_mask = bboxes.to_tensor(), tf.sequence_mask(bboxes.row_lengths())
        scores_tensor, scores_mask = scores.to_tensor(), tf.sequence_mask(scores.row_lengths())
        nmsed_bboxes, nmsed_scores, nmsed_classes, valid_detections = tf.image.combined_non_max_suppression(
            bboxes_tensor[:, :, tf.newaxis, :], scores_tensor[:, :, tf.newaxis], **self.non_max_suppression_config
        )
        return (
            tf.RaggedTensor.from_tensor(nmsed_bboxes, lengths=valid_detections),
            tf.RaggedTensor.from_tensor(nmsed_classes, lengths=valid_detections),
            tf.RaggedTensor.from_tensor(nmsed_scores, lengths=valid_detections),
        )

    @staticmethod
    def _cast(bboxes, classes, scores):
        # make widths the first values in bboxes [x1, y1, x2, y2]
        switched_bboxes = tf.stack((bboxes[:, :, 1], bboxes[:, :, 0], bboxes[:, :, 3], bboxes[:, :, 2]), axis=2)
        return switched_bboxes, tf.cast(classes, tf.int32), scores


class EfficientDetD6(EfficientDet):
    model_path = "efficientdet-d6"


class EfficientDetD5AdvPropAA(EfficientDet):
    model_path = "efficientdet-d5-advprop-aa"
