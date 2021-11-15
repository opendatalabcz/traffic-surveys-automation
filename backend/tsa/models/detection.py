from abc import abstractmethod
from urllib.parse import urljoin

import tensorflow as tf
import tensorflow_hub as tf_hub

from tsa.constants import TF_HUB
from tsa.datasets.abstract import FramesDataset
from tsa.models.abstract import PredictableModel


class DetectionModel(PredictableModel):
    model_url: str
    filtered_labels: tf.Tensor

    def __init__(
        self,
        max_outputs: int = 100,
        iou_threshold: float = 0.5,
        score_threshold: float = 0.5,
    ):
        # download the model
        self.model = tf_hub.load(urljoin(TF_HUB, self.model_url))
        # define non-max-suppression config
        self.non_max_suppression_config = {
            "max_output_size": max_outputs,
            "iou_threshold": iou_threshold,
            "score_threshold": score_threshold,
        }
        # constant for filtering
        self.tile_multiples = [1, tf.shape(self.filtered_labels)[0]]

    def predict(self, dataset: FramesDataset):
        for frame in dataset.frames:
            yield self._predict(frame)

    def _predict(self, frame):
        prediction = self.model([frame])
        bboxes, classes, scores = self._get(prediction)
        bboxes, classes, scores = self._cast(bboxes, classes, scores)
        bboxes, classes, scores = self._filter(bboxes, classes, scores)
        bboxes, classes, scores = self._apply_non_max_suppression(bboxes, classes, scores)
        return frame, bboxes, classes, scores

    @abstractmethod
    def _get(self, prediction):
        pass

    @abstractmethod
    def _cast(self, bboxes, classes, scores):
        pass

    def _filter(self, bboxes, classes, scores):
        mask = tf.tile(tf.expand_dims(classes, -1), self.tile_multiples)
        mask = tf.reduce_any(tf.equal(mask, self.filtered_labels), -1)
        return tf.boolean_mask(bboxes, mask), tf.boolean_mask(classes, mask), tf.boolean_mask(scores, mask)

    def _apply_non_max_suppression(self, bboxes, classes, scores):
        non_max_suppression = tf.image.non_max_suppression(bboxes, scores, **self.non_max_suppression_config)
        return (
            tf.gather(bboxes, non_max_suppression),
            tf.gather(classes, non_max_suppression),
            tf.gather(scores, non_max_suppression),
        )


class FasterRCNNResnet(DetectionModel):
    model_url = "tensorflow/faster_rcnn/resnet152_v1_1024x1024/1"
    filtered_labels = tf.constant([2, 3, 4, 6, 8])

    def _get(self, prediction):
        return prediction["detection_boxes"][0], prediction["detection_classes"][0], prediction["detection_scores"][0]

    def _cast(self, bboxes, classes, scores):
        return bboxes, tf.cast(classes, tf.int32), scores
