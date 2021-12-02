from abc import abstractmethod
from typing import Any, List, Tuple

from tsa.datasets.abstract import FramesDataset
from tsa.bbox import BBox


class PredictableModel:
    @abstractmethod
    def predict(self, dataset: FramesDataset) -> Tuple[Any, List[BBox], Any, Any]:
        pass
