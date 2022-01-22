import cv2
import numpy as np

from tsa import np_utils, typing

from .abstract import StorageMethod


class VideoStorageMethod(StorageMethod):
    def __init__(self, path: str, frame_rate: float, resolution: typing.IMAGE_SHAPE):
        self.output_video = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), frame_rate, resolution)
        self.id_color_mapping = {}

    def save_frame(self, frame, detections, identifiers, classes, scores):
        for detection, identifier, class_, score in zip(detections, identifiers, classes, scores):
            color = (255, 255, 255)
            np_detection = detection.numpy().astype(np.int32)

            if identifier is not None:
                color = self.id_color_mapping.get(identifier, np_utils.generate_color())
                self.id_color_mapping[identifier] = color

            cv2.rectangle(frame, (np_detection[0], np_detection[1]), (np_detection[2], np_detection[3]), color, 2, 1)

            if class_ is not None:
                text = f"{class_}: {score}"
                cv2.putText(frame, text, (np_detection[0], np_detection[1]), cv2.FONT_HERSHEY_PLAIN, 1, color)

        self.output_video.write(frame)

    def close(self):
        self.output_video.release()
