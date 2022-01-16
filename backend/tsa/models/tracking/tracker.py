from enum import Enum
from uuid import uuid4

import numpy as np
from scipy.linalg import solve_triangular

from tsa import typing, bbox
from tsa.cv2.kalman_filter import KalmanFilter


class TrackerState(Enum):
    new = "new"
    active = "active"
    deleted = "deleted"


class Tracker:
    def __init__(self, initial_position: typing.BBOX_COORDINATES, min_updates: int, max_age: int):
        self.id = uuid4()
        self.updates, self.predictions, self.time_since_update, self._status = 0, 0, 0, TrackerState.new
        self.min_updates, self.max_time_since_update = min_updates, max_age
        self.kalman_filter = KalmanFilter(bbox.bbox_to_center(initial_position))

    @property
    def state(self) -> typing.BBOX_COORDINATES:
        bbox_prediction, _ = bbox.center_to_bbox(self.kalman_filter.state)
        return bbox_prediction

    @property
    def is_active(self) -> bool:
        return self._status == TrackerState.active

    @property
    def is_deleted(self) -> bool:
        return self._status == TrackerState.deleted

    def update(self, new_position: typing.BBOX_COORDINATES):
        self.updates += 1
        self.time_since_update = 0

        self.kalman_filter.update(bbox.bbox_to_center(new_position))

        if self._status == TrackerState.new and self.updates >= self.min_updates:
            self._status = TrackerState.active

    def predict(self) -> typing.BBOX_COORDINATES:
        self.predictions += 1
        self.time_since_update += 1

        prediction = self.kalman_filter.predict()
        bbox_prediction, _ = bbox.center_to_bbox(prediction)
        return bbox_prediction


class DeepTracker(Tracker):
    def __init__(self, initial_position: typing.BBOX_COORDINATES, min_updates: int, max_age: int, feature=None):
        super().__init__(initial_position, min_updates, max_age)

        self.features = [feature] if feature is not None else []

    def update_with_feature(self, new_position: typing.BBOX_COORDINATES, feature):
        super().update(new_position)

        self.features.append(feature)

    def mark_missed(self):
        if self._status == TrackerState.new:
            self._status = TrackerState.deleted
        elif self.time_since_update > self.max_time_since_update:
            self._status = TrackerState.deleted

    def mahalanobis_distance(self, measurements, only_position=False):
        """Compute Mahalanobis distance between state distribution and measurements."""
        mean, covariance = self.kalman_filter.state, self.kalman_filter.covariance

        if only_position:
            mean, covariance = mean[:2], covariance[:2, :2]
            measurements = measurements[:, :2]

        d = solve_triangular(
            np.linalg.cholesky(covariance), (measurements - mean).T, lower=True, check_finite=False, overwrite_b=True
        )
        return np.sum(d * d, axis=0)
