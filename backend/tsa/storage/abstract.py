from abc import ABC, abstractmethod

from tsa.dataclasses.track import Track


class WriteStorageMethod(ABC):
    @abstractmethod
    def save_frame(self, frame, detections, identifiers, classes, scores):
        ...

    @abstractmethod
    def close(self):
        ...


class ReadStorageMethod(ABC):
    @abstractmethod
    def read_track(self) -> Track:
        ...
