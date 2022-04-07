from typing import Sequence

import numpy as np
from shapely.geometry import LineString, Point


class Line(LineString):
    @classmethod
    def from_points(cls, points: Sequence[Point]) -> "Line":
        return cls([(point.x, point.y) for point in points])

    @property
    def coordinates(self):
        return np.asarray(self.coords)
