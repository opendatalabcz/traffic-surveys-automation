import tensorflow as tf

from tsa.dataclasses.frames import FramesDataset
from tsa.models.abstract import PredictableModel, TrackableModel
from tsa.monitoring import Monitor


def run_detection_and_tracking(
    dataset: FramesDataset, detection_model: PredictableModel, tracking_model: TrackableModel
):
    """Run provided detection and tracking models on the dataset.

    @return: generator of tuples numpy frame, detections in frame (None x 4), identifications, classes and scores
    """
    detection_function = Monitor.monitor_duration(detection_model.predict, "detection")
    tracking_function = Monitor.monitor_duration(tracking_model.track, "tracking")

    for frames, batch_detections, batch_classes, batch_scores in detection_function(dataset):
        batch_tracking = tracking_function(batch_detections, frames=frames)

        for frame, detections, classes, scores, (tracks, identifiers, new_tracks) in zip(
            frames, batch_detections, batch_classes, batch_scores, batch_tracking
        ):
            # pad the detection outputs to match the tracks and identifiers shape
            padding_shape = tf.constant([[0, new_tracks]])
            padded_classes = tf.pad(classes, padding_shape, constant_values=0)
            padded_scores = tf.pad(scores, padding_shape, constant_values=0.0)
            # merge detections and tracks in a way that detected bounding boxes are considered to be a ground truth
            merged_detections = tf.concat((detections, tracks[detections.shape[0] :]), axis=0)

            yield frame.numpy(), merged_detections, identifiers, padded_classes, padded_scores
