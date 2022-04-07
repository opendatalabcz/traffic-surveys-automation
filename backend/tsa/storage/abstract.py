from abc import ABC, abstractmethod
from typing import Generator

from tsa import typing
from tsa.dataclasses.track import FinalTrack


class FrameStorageMethod(ABC):
    @abstractmethod
    def draw_objects(self, frame, detections, identifiers, classes, scores) -> typing.NP_FRAME:
        ...


class WriteStorageMethod(ABC):
    @abstractmethod
    def save_frame(self, frame, detections, identifiers, classes, scores) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...


class ReadStorageMethod(ABC):
    @property
    @abstractmethod
    def track_name(self) -> str:
        ...

    @abstractmethod
    def read_track(self) -> Generator[FinalTrack, None, None]:
        ...
