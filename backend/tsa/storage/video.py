from pathlib import Path

import cv2

from tsa import np_utils, typing

from .abstract import WriteStorageMethod


class VideoStorageMethod(WriteStorageMethod):
    def __init__(self, path: Path, frame_rate: float, resolution: typing.IMAGE_SHAPE, show_class: bool):
        self.show_class = show_class
        self.id_color_mapping = {}
        self.color_generator = np_utils.RandomGenerator(str(path))
        self.output_video = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), frame_rate, resolution)

    def draw_objects(self, frame, detections, identifiers, classes, scores):
        for detection, identifier, class_, score in zip(detections, identifiers, classes, scores):
            color = (255, 255, 255)

            if identifier is not None:
                color = self.id_color_mapping.get(identifier, self.color_generator.colors(1)[0])
                self.id_color_mapping[identifier] = color

            cv2.rectangle(frame, (detection[0], detection[1]), (detection[2], detection[3]), color, 2, 1)

            if self.show_class and class_ is not None:
                text = f"{class_}: {score}"
                cv2.putText(frame, text, (detection[0], detection[1]), cv2.FONT_HERSHEY_PLAIN, 1, color)

        return frame

    def save_frame(self, frame, detections, identifiers, classes, scores):
        frame_with_objects = self.draw_objects(frame, detections, identifiers, classes, scores)
        self.output_video.write(frame_with_objects)

    def close(self):
        self.output_video.release()
