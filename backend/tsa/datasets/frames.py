from abc import abstractmethod
from typing import Generator, Optional

import tensorflow as tf

from tsa import typing
from tsa.cv2.video_capture import VideoCapture


class FramesDataset:
    output_shape = (None, None, 3)
    output_tf_dtype = tf.uint8

    @property
    @abstractmethod
    def frames(self) -> Generator[typing.NP_FRAME, None, None]:
        pass

    def as_tf_dataset(self, batch_size: int) -> tf.data.Dataset:
        dataset = tf.data.Dataset.from_generator(
            lambda: self.frames,
            output_signature=tf.TensorSpec(self.output_shape, dtype=self.output_tf_dtype),
        )
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        dataset = dataset.batch(batch_size)
        return dataset


class VideoFramesDataset(FramesDataset):
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
        with VideoCapture(self.file_path) as video:
            # compute the rate at which the frames are yielded
            frame_rate = int(video.frame_rate / (self.frame_rate or video.frame_rate))

            for frame in video.read_frames(frame_rate):
                yielded_frames += 1
                yield frame
                if self._stop(yielded_frames):
                    break

    def _stop(self, current_frame: int) -> bool:
        return self.max_frames is not None and current_frame >= self.max_frames
