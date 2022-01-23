from dataclasses import dataclass
from typing import List

import numpy as np

from tsa import bbox


@dataclass
class Track:
    identifier: str
    path: List

    _score_sum: float

    @property
    def count(self) -> int:
        return len(self.path)

    @property
    def average_score(self) -> float:
        tf_average_score = self._score_sum / self.count
        return float(tf_average_score)

    def __init__(self, identifier: str):
        self.path = []
        self.identifier = identifier
        self._score_sum = 0.0

    def update(self, new_detection, new_score):
        self._score_sum += new_score

        new_detection_centered = bbox.bbox_to_center(new_detection)
        new_detection_coordinates = new_detection_centered[:2]
        self.path.append(new_detection_coordinates)

    def as_dict(self):
        return {"identifier": str(self.identifier), "score": self.average_score, "path": np.asarray(self.path).tolist()}
