from abc import abstractmethod
from collections import namedtuple
from pathlib import Path
from typing import Generator, Optional

import tensorflow as tf

from tsa import typing
from tsa.cv2.video_capture import VideoCapture

VideoStatistics = namedtuple("VideoStatistics", ("frame_rate", "resolution"))


def get_frame_rate_for_video(video: VideoCapture, expected_frames: Optional[int]) -> int:
    if expected_frames is None or video.frame_rate < expected_frames:
        return 1

    return int(video.frame_rate / expected_frames)


class FramesDataset:
    output_tf_shape = (None, None, 3)
    output_tf_dtype = tf.uint8

    @property
    @abstractmethod
    def frames(self) -> Generator[typing.NP_FRAME, None, None]:
        pass

    @property
    @abstractmethod
    def video_statistics(self) -> VideoStatistics:
        pass

    def as_tf_dataset(self, batch_size: int) -> tf.data.Dataset:
        dataset = tf.data.Dataset.from_generator(
            lambda: self.frames,
            output_signature=tf.TensorSpec(self.output_tf_shape, dtype=self.output_tf_dtype),
        )
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        dataset = dataset.batch(batch_size)
        return dataset


class VideoFramesDataset(FramesDataset):
    def __init__(
        self, file_path: Path, output_frame_rate: Optional[int] = None, max_yielded_frames: Optional[int] = None
    ):
        """Initialize a dataset of video frames.

        @param file_path path to the video source
        @param output_frame_rate FPS of the yielded frames, FPS not changed if not provided
        @param max_yielded_frames maximum number of yielded frames
        """
        self.file_path = str(file_path)
        self.max_frames = max_yielded_frames
        self.output_frame_rate = output_frame_rate

    @property
    def frames(self) -> Generator[typing.NP_FRAME, None, None]:
        yielded_frames = 0
        with VideoCapture(self.file_path) as video:
            # compute the rate at which the frames are yielded
            frame_rate = get_frame_rate_for_video(video, self.output_frame_rate)

            for frame in video.read_frames(frame_rate):
                yielded_frames += 1
                yield frame
                if self._stop(yielded_frames):
                    break

    @property
    def video_statistics(self) -> VideoStatistics:
        with VideoCapture(self.file_path) as video:
            frame_rate = self.output_frame_rate

            if frame_rate is None or video.frame_rate < frame_rate:
                frame_rate = video.frame_rate

            return VideoStatistics(frame_rate=frame_rate, resolution=video.resolution)

    def _stop(self, current_frame: int) -> bool:
        return self.max_frames is not None and current_frame >= self.max_frames
