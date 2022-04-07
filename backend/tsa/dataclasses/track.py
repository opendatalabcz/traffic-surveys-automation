from typing import Any, Dict, List, Union
from uuid import UUID

import numpy as np

from tsa import bbox
from tsa.dataclasses.geometry import Curve


class Track:
    identifier: str
    frame_numbers: List[int]

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
        path = np.asarray(self._path)
        return path[:, :2]

    def __init__(self, identifier: Union[str, UUID], class_: int):
        self.identifier, self.frame_numbers = str(identifier), []
        self.class_ = class_
        self._path = []
        self._score_sum = 0.0

    def update(self, frame_number: int, new_detection, new_score):
        self.frame_numbers.append(frame_number)
        self._score_sum += new_score
        self._path.append(bbox.bbox_to_center(new_detection))

    def as_dict(self):
        return {
            "identifier": self.identifier,
            "class": self.class_,
            "score": self.average_score,
            "frames": self.frame_numbers,
            "path": np.asarray(self._path).tolist(),
        }


class FinalTrack(Track):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data["identifier"], data["class"])
        self.frame_numbers = data["frames"]

        self._path = data["path"]
        self._score_sum = data["score"] * self.count

        self.curve = Curve(self.path, 3, 50)

    def bounding_box(self, frame: int):
        index = frame - self.frame_numbers[0]
        return bbox.center_to_bbox(self._path[index])[0].astype(np.int32)
