from abc import ABC, abstractmethod


class StorageMethod(ABC):
    @abstractmethod
    def save_frame(self, frame, detections, identifiers, classes, scores):
        ...

    @abstractmethod
    def close(self):
        ...
