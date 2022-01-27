from dataclasses import dataclass
from typing import Optional

import numpy as np
from scipy.interpolate import make_lsq_spline

from tsa import typing


@dataclass
class SmoothingCurve:
    def __init__(self, fitting_points: typing.NP_ARRAY):
        self.count = fitting_points.shape[0]

        time = np.arange(0, self.count)
        self._interpolation_fn = make_lsq_spline(
            time,
            fitting_points,
            np.array([time[0] - 2, time[0] - 1, time[0], *time[1:-1:11], time[-1], time[-1] + 1, time[-1] + 2]),
            k=2,
        )

        self.start_point = self._interpolation_fn(0)
        self.end_point = self._interpolation_fn(self.count)

    def __call__(self, *args, **kwargs):
        return self._interpolation_fn(*args, **kwargs)

    @property
    def length(self) -> float:
        return np.linalg.norm(self.end_point - self.start_point)

    def points(self, length: int, start: int = 0, end: Optional[int] = None):
        return np.array([self._interpolation_fn(t) for t in np.linspace(start, end or self.count, length)])
