from dataclasses import dataclass

import numpy as np
from scipy.interpolate import make_lsq_spline

from tsa import typing


@dataclass
class FittingCurve:
    def __init__(self, fitting_points: typing.NP_ARRAY, degree: int):
        unique_x_data = np.arange(0, fitting_points.shape[0])

        self._x_start_point, self._x_end_point = np.min(unique_x_data), np.max(unique_x_data)
        self._interpolation_fn = make_lsq_spline(
            unique_x_data,
            fitting_points,
            np.array(
                [
                    unique_x_data[0],
                    unique_x_data[0],
                    unique_x_data[0],
                    *unique_x_data[2:-2:10],
                    unique_x_data[-1],
                    unique_x_data[-1],
                    unique_x_data[-1],
                ]
            ),
            k=2,
            check_finite=False,
        )

    # interp1d(unique_x_data, y_data[unique_x_data_index], kind="linear", fill_value="extrapolate", assume_sorted=False)

    def __call__(self, *args, **kwargs):
        return self._interpolation_fn(*args, **kwargs)

    @property
    def x_lin_space(self):
        return np.linspace(self._x_start_point, self._x_end_point, 100, dtype=np.int32)
