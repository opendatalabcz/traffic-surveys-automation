from typing import Sequence

import numpy as np
from shapely.geometry import LineString, Point


class Line(LineString):
    def __init__(self, coordinates):
        super().__init__(coordinates)

        self.start_point = Point(coordinates[0])
        self.end_point = Point(coordinates[-1])

    @classmethod
    def from_points(cls, points: Sequence[Point]) -> "Line":
        return cls([(point.x, point.y) for point in points])

    @property
    def coordinates(self):
        return np.asarray(self.coords)

    @property
    def vector(self):
        return Point(self.end_point.x - self.start_point.x, self.end_point.y - self.start_point.y)

    def angle(self, other: "Line"):
        nominator = self.vector.x * other.vector.x + self.vector.y * other.vector.y
        radial_angle = np.arccos(nominator / (self.length * other.length))
        return np.degrees(radial_angle)
