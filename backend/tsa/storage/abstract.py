from abc import ABC, abstractmethod
from typing import Generator

from tsa.dataclasses.track import FinalTrack


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
