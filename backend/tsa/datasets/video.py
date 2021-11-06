from typing import Generator, Optional

from tsa import typing
from tsa.cv2_utils import VideoCapture
from tsa.datasets.abstract import FramesDataset


class VideoDataset(FramesDataset):
    def __init__(
        self, file_path: str, output_frame_rate: Optional[int] = None, max_yielded_frames: Optional[int] = None
    ):
        """Initialize a dataset of video frames.

        @param file_path path to the video source
        @param output_frame_rate FPS of the yielded frames, FPS not changed if not provided
        @param max_yielded_frames maximum number of yielded frames
        """
        self.file_path = file_path
        self.max_frames = max_yielded_frames
        self.frame_rate = output_frame_rate

    @property
    def frames(self) -> Generator[typing.NP_FRAME, None, None]:
        yielded_frames = 0
        with VideoCapture.from_file(self.file_path) as video:
            # compute the rate at which the frames are yielded
            frame_rate = int(video.frame_rate / (self.frame_rate or video.frame_rate))

            for frame in video.read_frames(frame_rate):
                yielded_frames += 1
                yield frame
                if self._stop(yielded_frames):
                    break

    def _stop(self, current_frame: int) -> bool:
        return self.max_frames is not None and current_frame >= self.max_frames
