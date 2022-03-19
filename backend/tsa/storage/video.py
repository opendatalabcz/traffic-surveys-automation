import cv2
import numpy as np

from tsa import np_utils, typing

from .abstract import WriteStorageMethod


class VideoStorageMethod(WriteStorageMethod):
    def __init__(self, path: str, frame_rate: float, resolution: typing.IMAGE_SHAPE, show_class: bool):
        self.output_video = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), frame_rate, resolution)
        self.id_color_mapping = {}
        self.color_generator = np_utils.RandomGenerator(path)
        self.show_class = show_class

    def save_frame(self, frame, detections, identifiers, classes, scores):
        for detection, identifier, class_, score in zip(detections, identifiers, classes, scores):
            color = (255, 255, 255)
            np_detection = detection.numpy().astype(np.int32)

            if identifier is not None:
                color = self.id_color_mapping.get(identifier, self.color_generator.colors(1)[0])
                self.id_color_mapping[identifier] = color

            cv2.rectangle(frame, (np_detection[0], np_detection[1]), (np_detection[2], np_detection[3]), color, 2, 1)

            if self.show_class and class_ is not None:
                text = f"{class_}: {score}"
                cv2.putText(frame, text, (np_detection[0], np_detection[1]), cv2.FONT_HERSHEY_PLAIN, 1, color)

        self.output_video.write(frame)

    def close(self):
        self.output_video.release()
