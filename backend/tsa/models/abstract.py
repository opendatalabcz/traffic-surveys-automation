from abc import abstractmethod
from typing import Any, List, Tuple

from tsa.datasets import FramesDataset


class PredictableModel:
    def __init__(self):
        self.model = self._build_model()

    @abstractmethod
    def predict(self, dataset: FramesDataset) -> Tuple[Any, Any, Any, Any]:
        pass

    @abstractmethod
    def _build_model(self):
        pass


class TrackableModel:
    @abstractmethod
    def track(self, detections, **kwargs):
        pass
