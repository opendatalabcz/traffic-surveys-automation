from urllib.parse import urljoin

import tensorflow as tf
import tensorflow_hub as tf_hub

from tsa.constants import TF_HUB
from tsa.datasets.abstract import FramesDataset
from tsa.enums import DetectionModelType
from tsa.models.abstract import PredictableModel


class DetectionModel(PredictableModel):
    def __init__(
        self,
        model: DetectionModelType,
        max_outputs: int = 100,
        iou_threshold: float = 0.5,
        score_threshold: float = 0.5,
    ):
        # download the model
        self.model = tf_hub.load(urljoin(TF_HUB, model.value))
        # define non-max-suppression config
        self.config = {
            "max_output_size": max_outputs,
            "iou_threshold": iou_threshold,
            "score_threshold": score_threshold,
        }
        # define constants
        self.filtered_labels = tf.constant([2, 3, 4, 6, 8])
        self.tile_multiples = [1, tf.shape(self.filtered_labels)[0]]

    def predict(self, dataset: FramesDataset):
        for frame in dataset.frames:
            yield self._predict(frame)

    def _predict(self, frame):
        prediction = self.model([frame])
        bboxes, classes, scores = (
            prediction["detection_boxes"][0],
            prediction["detection_classes"][0],
            prediction["detection_scores"][0],
        )
        bboxes, classes, scores = self._cast(bboxes, classes, scores)
        bboxes, classes, scores = self._filter(bboxes, classes, scores)
        bboxes, classes, scores = self._apply_non_max_suppression(bboxes, classes, scores)
        return frame, bboxes, classes, scores

    @staticmethod
    def _cast(bboxes, classes, scores):
        return bboxes, tf.cast(classes, tf.int32), scores

    def _filter(self, bboxes, classes, scores):
        mask = tf.tile(tf.expand_dims(classes, -1), self.tile_multiples)
        mask = tf.reduce_any(tf.equal(mask, self.filtered_labels), -1)
        return tf.boolean_mask(bboxes, mask), tf.boolean_mask(classes, mask), tf.boolean_mask(scores, mask)

    def _apply_non_max_suppression(self, bboxes, classes, scores):
        non_max_suppression = tf.image.non_max_suppression(bboxes, scores, **self.config)
        return (
            tf.gather(bboxes, non_max_suppression),
            tf.gather(classes, non_max_suppression),
            tf.gather(scores, non_max_suppression),
        )
