from typing import Optional

import numpy as np
from scipy.interpolate import make_lsq_spline

from tsa import typing

from .line import Line


class LeastSquaresInterpolation:
    def __init__(self, interpolation_points: typing.NP_ARRAY, degree: int, knot_step: int):
        self.length = interpolation_points.shape[0]

        time = np.arange(0, self.length)
        self._interpolation_fn = make_lsq_spline(
            time, interpolation_points, self._create_knots(time, degree, knot_step), k=degree
        )

    def interpolating_points(self, length: int, start: int = 0, end: Optional[int] = None):
        time_range = np.linspace(start, end or self.length, length)

        return np.array([self._interpolation_fn(t) for t in time_range])

    @staticmethod
    def _create_knots(time, degree: int, knot_step: int):
        start_knots = [time[0] - i for i in reversed(range(degree + 1))]
        end_knots = [time[-1] + i for i in range(degree + 1)]

        return np.array([*start_knots, *time[1:-1:knot_step], *end_knots])


class Curve(Line):
    def __init__(self, coordinates: typing.NP_ARRAY, interpolation_degree: int, interpolation_detail: int):
        interpolation = LeastSquaresInterpolation(coordinates, interpolation_degree, 13)

        super().__init__(interpolation.interpolating_points(interpolation_detail))
