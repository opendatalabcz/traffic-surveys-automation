from typing import Any, Dict, List, Union
from uuid import UUID

import numpy as np

from tsa import bbox
from tsa.dataclasses.geometry import Curve


class Track:
    identifier: str

    _path: List
    _score_sum: float

    @property
    def count(self) -> int:
        return len(self._path)

    @property
    def average_score(self) -> float:
        tf_average_score = self._score_sum / self.count
        return float(tf_average_score)

    @property
    def path(self):
        return np.asarray(self._path)

    def __init__(self, identifier: Union[str, UUID]):
        self.identifier = str(identifier)
        self._path = []
        self._score_sum = 0.0

    def update(self, new_detection, new_score):
        self._score_sum += new_score

        new_detection_centered = bbox.bbox_to_center(new_detection)
        new_detection_coordinates = new_detection_centered[:2]
        self._path.append(new_detection_coordinates)

    def as_dict(self):
        return {"identifier": self.identifier, "score": self.average_score, "path": self.path.tolist()}


class FinalTrack(Track):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data["identifier"])
        self._path = data["path"]
        self._score_sum = data["score"] * self.count

        self.curve = Curve(self.path, 3, 50)
