from typing import Tuple

import cv2
import numpy as np
import tensorflow as tf

from tsa.datasets import FramesDataset
from tsa.models.abstract import PredictableModel, TrackableModel


def get_new_color():
    return tuple(np.random.random(size=3) * 256)


def save_as_video(
    prediction_model: PredictableModel,
    tracking_model: TrackableModel,
    dataset: FramesDataset,
    video_name: str,
    video_frame_rate: int,
    video_resolution: Tuple[int, int],  # resolution in form (width, height)
):
    identifiers_to_colors_mapping = {}
    output = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*"mp4v"), float(video_frame_rate), video_resolution)

    for frames, batch_bboxes, batch_classes, batch_scores in prediction_model.predict(dataset):
        for (detections, identifiers, new_boxes), frame, bboxes, classes, scores in zip(
            tracking_model.track(batch_bboxes, frames=frames), frames, batch_bboxes, batch_classes, batch_scores
        ):
            frame = frame.numpy()
            bboxes = tf.concat((bboxes, tf.zeros((new_boxes, 4))), axis=0)
            classes = tf.concat((classes, tf.zeros((new_boxes,), dtype=tf.int32)), axis=0)
            scores = tf.concat((scores, tf.zeros((new_boxes,))), axis=0)
            for bbox, detection, identifier, class_, score in zip(bboxes, detections, identifiers, classes, scores):
                color = (255, 255, 255)

                if identifier is not None:
                    color = identifiers_to_colors_mapping.get(identifier, get_new_color())
                    identifiers_to_colors_mapping[identifier] = color
                if detection is not None:
                    detection_rectangle = detection.astype(np.int32)
                    cv2.rectangle(
                        frame,
                        (detection_rectangle[0], detection_rectangle[1]),
                        (detection_rectangle[2], detection_rectangle[3]),
                        color,
                        2,
                        1,
                    )
                if bbox is not None:
                    bbox = bbox.numpy().astype(np.int32)
                    cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2, 1)
                    cv2.putText(
                        frame,
                        f"{class_}: {score}",
                        (bbox[0], bbox[1]),
                        cv2.FONT_HERSHEY_PLAIN,
                        1,
                        color,
                    )
            output.write(frame)

    output.release()
