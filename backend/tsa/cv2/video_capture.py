from typing import Generator, Tuple

import cv2

from tsa.typing import NP_FRAME


class VideoCapture:
    def __init__(self, file_path: str):
        self._read_frames = 0
        self._video = cv2.VideoCapture(file_path)

    @property
    def frame_rate(self) -> float:
        return self._video.get(cv2.CAP_PROP_FPS)

    @property
    def resolution(self) -> Tuple[int, int]:
        """Video resolution as (width, height)."""
        width = self._video.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self._video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return int(width), int(height)

    def read_frames(self, rate: int = 1) -> Generator[NP_FRAME, None, None]:
        while True:
            read, frame = self._video.read()
            if read:
                if self._read_frames % rate == 0:
                    yield frame
                self._read_frames += 1
            else:
                break

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._video.release()
