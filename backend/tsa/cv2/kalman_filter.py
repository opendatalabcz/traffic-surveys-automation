from collections import namedtuple

import cv2
import numpy as np

from tsa import typing
from tsa.np_utils import diagonal


KalmanFilterStaticMatrices = namedtuple(
    "KalmanFilterStaticMatrices",
    ["measurement_matrix", "measurement_noise_cov", "transition_matrix", "process_noise_cov"],
)


class KalmanFilter:
    """Kalman filter implementation for keeping track of vehicles by updating and predicting the position.

    - measurement: 4 values: center_x, center_y, ratio, height
    - state: 10 values: center_x, center_y, ratio, height, *velocity_of_each_measurement, x_acceleration, y_acceleration
    """
    static_matrices: KalmanFilterStaticMatrices = None

    def __init__(self, initial_position: typing.BBOX_CENTER):
        # init kalman filter and its initial values
        self.kalman_filter = cv2.KalmanFilter(dynamParams=10, measureParams=4)
        self._init_variables(
            initial_position, delta=1.0, position_measurement_var=9.0, size_measurement_var=25.0, acceleration_var=0.15
        )

    @property
    def state(self) -> typing.BBOX_CENTER:
        return self.kalman_filter.statePost[:4].reshape(-1,)

    @property
    def covariance(self):
        return self.kalman_filter.errorCovPost

    def update(self, new_measurement: typing.BBOX_CENTER):
        self.kalman_filter.correct(new_measurement)

    def predict(self) -> typing.BBOX_CENTER:
        prediction = self.kalman_filter.predict()
        prediction = prediction.reshape(-1,)
        return prediction[:4]

    def _init_variables(self, initial_position: typing.BBOX_CENTER, **kwargs):
        self._init_static_matrices(**kwargs)

        self.kalman_filter.transitionMatrix = self.static_matrices.transition_matrix
        self.kalman_filter.measurementMatrix = self.static_matrices.measurement_matrix
        self.kalman_filter.processNoiseCov = self.static_matrices.process_noise_cov
        self.kalman_filter.measurementNoiseCov = self.static_matrices.measurement_noise_cov

        # set initial state value
        self.kalman_filter.statePost = np.array([*initial_position, 0, 0, 0, 0, 0, 0], dtype=np.float32).reshape(-1, 1)

        # set initial error covariance matrix
        std_position_weight, std_velocity_weight, height = 1.0 / 20, 1.0 / 160, initial_position[3]
        self.kalman_filter.errorCovPost = diagonal(100.0, 1_000.0, repeats=(4, 6))

    @classmethod
    def _init_static_matrices(
        cls, delta: float, position_measurement_var: float, size_measurement_var: float, acceleration_var: float
    ):
        """Initialize static Kalman filter matrices.

        The following matrices are configured:
        - measurement (observation) matrix H (4 x 10): ones on the main diagonal
        - measurement uncertainty matrix R (4 x 4): diagonal matrix (measurement uncertainties independent)
        - transition matrix F (10 x 10): ones on diagonal, t on velocity positions, 0.5t^2 on acceleration positions
        - process noise cov matrix Q (10 x 10): non-zero on dependant positions
        """
        if cls.static_matrices is not None:
            return

        transition_matrix = np.eye(10, 10, dtype=np.float32)
        transition_matrix[0:4, 4:8] = np.eye(4, 4) * delta
        transition_matrix[0:2, 8:10] = np.eye(2, 2) * 0.5 * delta ** 2

        process_noise_covariance = diagonal(delta ** 4 / 4, delta ** 2, 1, repeats=(4, 4, 2))
        process_noise_covariance[0:4, 4:8] = process_noise_covariance[4:8, 0:4] = diagonal(delta ** 3 / 2, repeats=4)
        process_noise_covariance[0:2, 8:10] = process_noise_covariance[8:10, 0:2] = diagonal(delta ** 2 / 2, repeats=2)
        process_noise_covariance[4:6, 8:10] = process_noise_covariance[8:10, 4:6] = diagonal(delta, repeats=2)

        cls.static_matrices = KalmanFilterStaticMatrices(
            np.eye(4, 10, dtype=np.float32),
            diagonal(position_measurement_var, size_measurement_var, repeats=(2, 2)),
            transition_matrix,
            process_noise_covariance * acceleration_var
        )
