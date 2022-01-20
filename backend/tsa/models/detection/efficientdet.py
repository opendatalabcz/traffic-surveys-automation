from abc import ABC
from typing import Generator

import tensorflow as tf
import tensorflow_hub as tf_hub

from tsa.config import config
from tsa.datasets import FramesDataset
from tsa.models import PredictableModel


class EfficientDet(PredictableModel, ABC):
    model_path: str

    def __init__(
        self, max_outputs: int, iou_threshold: float, score_threshold: float, nms_sigma: float, batch_size: int
    ):
        super().__init__()
        self.batch_size = batch_size
        # define non-max-suppression config
        self.non_max_suppression_config = {
            "max_output_size": max_outputs,
            "iou_threshold": iou_threshold,
            "score_threshold": score_threshold,
            "soft_nms_sigma": nms_sigma / 2,
            "pad_to_max_output_size": True,
        }
        # constant for filtering
        self.filtered_labels = tf.constant([2, 3, 4, 6, 8])
        self.tile_multiples = [1, 1, tf.shape(self.filtered_labels)[0]]

    def predict(self, dataset: FramesDataset) -> Generator:
        """Run a prediction step on a single batch and yield results.

        @return: generator of tuples:
        (frames [BATCH, W, H, 3], bounding boxes [BATCH, None, 4], classes [BATCH, None], scores [BATCH, None])
        """
        tf_dataset = dataset.as_tf_dataset(self.batch_size)

        for frames in tf_dataset:
            batch_bboxes, batch_classes, batch_scores = self._predict(frames)
            yield frames, batch_bboxes, batch_classes, batch_scores

    def _build_model(self):
        saved_model = tf_hub.load(f"{config.MODELS_PATH}/{self.model_path}")
        return saved_model.signatures["serving_default"]

    @tf.function()
    def _predict(self, frames):
        predictions = self.model(frames)
        bboxes, classes, scores = self._get(predictions)
        bboxes, classes, scores = self._filter(bboxes, classes, scores)
        bboxes, classes, scores = self._apply_non_max_suppression(bboxes, classes, scores)
        # switch width and height dimensions
        bboxes = tf.stack((bboxes[:, :, 1], bboxes[:, :, 0], bboxes[:, :, 3], bboxes[:, :, 2]), axis=2)
        return bboxes, classes, scores

    @staticmethod
    def _get(prediction):
        detections = prediction["detections:0"]
        return detections[:, :, 1:5], tf.cast(detections[:, :, 6], tf.int32), detections[:, :, 5]

    def _filter(self, bboxes, classes, scores):
        mask = tf.tile(tf.expand_dims(classes, -1), self.tile_multiples)
        mask = tf.reduce_any(tf.equal(mask, self.filtered_labels), -1)
        # replace score of other than vehicle labels with 0.0
        return bboxes, classes, tf.where(mask, x=scores, y=0.0)

    def _apply_non_max_suppression(self, bboxes, classes, scores):
        def single_non_max_suppression(input_elements):
            indices, single_scores, outputs = tf.raw_ops.NonMaxSuppressionV5(
                boxes=input_elements[0], scores=input_elements[2], **self.non_max_suppression_config
            )
            return tf.gather(input_elements[0], indices), tf.gather(input_elements[1], indices), single_scores, outputs

        nms_bboxes, nms_classes, nms_scores, valid_outputs = tf.vectorized_map(
            single_non_max_suppression, (bboxes, classes, scores)
        )
        return (
            tf.RaggedTensor.from_tensor(nms_bboxes, valid_outputs),
            tf.RaggedTensor.from_tensor(nms_classes, valid_outputs),
            tf.RaggedTensor.from_tensor(nms_scores, valid_outputs),
        )


class EfficientDetD6(EfficientDet):
    model_path = "efficientdet-d6"


class EfficientDetD5AdvPropAA(EfficientDet):
    model_path = "efficientdet-d5-advprop-aa"
