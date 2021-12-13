from typing import Tuple

import cv2
import numpy as np

from tsa.datasets.abstract import FramesDataset
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

    for frame, bboxes, classes, scores in prediction_model.predict(dataset):
        detections, identifiers = tracking_model.track(bboxes)
        for bbox, detection, identifier in zip(bboxes, detections, identifiers):
            bbox_rectangle = bbox.to_rectangle()
            detection_rectangle = detection.astype(np.int32)
            color = identifiers_to_colors_mapping.get(identifier, get_new_color())
            identifiers_to_colors_mapping[identifier] = color

            cv2.rectangle(
                frame,
                (detection_rectangle[0], detection_rectangle[1]),
                (detection_rectangle[2], detection_rectangle[3]),
                (255, 255, 255),
                1,
                1,
            )
            cv2.rectangle(
                frame, (bbox_rectangle[0], bbox_rectangle[1]), (bbox_rectangle[2], bbox_rectangle[3]), color, 2, 1
            )
        output.write(frame)

    output.release()