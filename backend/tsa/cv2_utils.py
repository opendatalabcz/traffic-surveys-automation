from contextlib import contextmanager
from typing import Generator

import cv2

from tsa.typing import NP_FRAME


class VideoCapture:
    def __init__(self, file_path: str):
        self._read_frames = 0
        self._video = cv2.VideoCapture(file_path)

    @classmethod
    @contextmanager
    def from_file(cls, file_path: str) -> "VideoCapture":
        video_capture = cls(file_path)
        try:
            yield video_capture
        finally:
            video_capture.release()

    @property
    def frame_rate(self) -> float:
        return self._video.get(cv2.CAP_PROP_FPS)

    def read_frames(self, rate: int = 1) -> Generator[NP_FRAME, None, None]:
        while True:
            read, frame = self._video.read()
            if read:
                if self._read_frames % rate == 0:
                    yield frame
                self._read_frames += 1
            else:
                break

    def release(self):
        self._video.release()
