from typing import Tuple

import cv2

from tsa.datasets.abstract import FramesDataset
from tsa.models.abstract import PredictableModel


def save_as_video(
    model: PredictableModel,
    dataset: FramesDataset,
    video_name: str,
    video_frame_rate: int,
    video_resolution: Tuple[int, int],  # resolution in form (width, height)
):
    output = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*"mp4v"), float(video_frame_rate), video_resolution)

    for frame, bboxes, classes, scores in model.predict(dataset):
        for bbox in bboxes:
            cv2.rectangle(frame, *bbox.to_numpy_rectangle(), (255, 0, 0), 1, 1)
        output.write(frame)

    output.release()
