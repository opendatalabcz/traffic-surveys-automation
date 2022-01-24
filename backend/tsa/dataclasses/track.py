from dataclasses import dataclass
from typing import List, Optional, Union
from uuid import UUID

import numpy as np

from tsa import bbox
from tsa.config import config

from .curve import FittingCurve


@dataclass
class Track:
    identifier: str

    _path: List
    _score_sum: float
    _polynomial_line: Optional[FittingCurve] = None

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

    @property
    def interpolation(self) -> FittingCurve:
        if self._polynomial_line is None:
            self._polynomial_line = FittingCurve(self.path, config.INTERPOLATION_POLYNOMIAL_DEGREE)

        return self._polynomial_line

    def __init__(self, identifier: Union[str, UUID]):
        self._path = []
        self.identifier = str(identifier)
        self._score_sum = 0.0

    def update(self, new_detection, new_score):
        self._score_sum += new_score

        new_detection_centered = bbox.bbox_to_center(new_detection)
        new_detection_coordinates = new_detection_centered[:2]
        self._path.append(new_detection_coordinates)

    @classmethod
    def from_dict(cls, data):
        new_object = cls(data["identifier"])
        new_object._path = data["path"]
        new_object._score_sum = data["score"] * new_object.count
        return new_object

    def as_dict(self):
        return {"identifier": self.identifier, "score": self.average_score, "path": self.path.tolist()}
