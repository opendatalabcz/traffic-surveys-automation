from typing import Tuple

import cv2
import numpy as np

from tsa.datasets.abstract import FramesDataset
from tsa.models.abstract import PredictableModel


def save_as_video(
    model: PredictableModel,
    dataset: FramesDataset,
    video_name: str,
    video_frame_rate: int,
    video_resolution: Tuple[int, int],  # resolution in form (width, height)
):
    output = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*"mp4v"), video_frame_rate, video_resolution)

    for frame, bboxes, classes, scores in model.predict(dataset):
        bboxes = bboxes.numpy() * np.array([*reversed(video_resolution), *reversed(video_resolution)])
        bboxes = bboxes.astype(np.int32)
        for bbox in bboxes:
            y1, x1, y2, x2 = bbox
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 1, 1)
        output.write(frame)

    output.release()
