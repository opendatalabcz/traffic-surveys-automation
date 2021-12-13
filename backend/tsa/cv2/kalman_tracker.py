from uuid import uuid4

import cv2
import numpy as np

from tsa.bbox import bbox_to_center, center_to_bbox
from tsa.np_utils import diagonal

KF_DIMENSION_PARAMS = 7
KF_MEASUREMENT_PARAMS = 4


class KalmanTracker:
    def __init__(self, initial_bbox):
        # init identifiers and counters
        self.id = uuid4()
        self.hit_streak = 0
        self.time_since_update = 0
        # init kalman filter and its initial values
        self.kalman_filter = cv2.KalmanFilter(dynamParams=KF_DIMENSION_PARAMS, measureParams=KF_MEASUREMENT_PARAMS)
        self._init_kalman_filter_variables(bbox_to_center(initial_bbox))

    @property
    def state(self):
        bbox, _ = center_to_bbox(self.kalman_filter.statePost[:4])
        return bbox

    def update(self, bbox):
        self.hit_streak += 1
        self.time_since_update = 0
        self.kalman_filter.correct(bbox_to_center(bbox))

    def predict(self):
        if self.time_since_update > 0:
            self.hit_streak = 0
        self.time_since_update += 1
        prediction = self.kalman_filter.predict().reshape(1, -1)
        prediction, _ = center_to_bbox(prediction[0][:4])
        return prediction

    def _init_kalman_filter_variables(self, state_center):
        self.kalman_filter.measurementMatrix = np.eye(KF_MEASUREMENT_PARAMS, KF_DIMENSION_PARAMS, dtype=np.float32)
        self.kalman_filter.measurementNoiseCov = diagonal(1.0, 10.0, repeats=(2, 2))
        self.kalman_filter.errorCovPost = diagonal(10.0, 10_000.0, repeats=(3, 4))
        self.kalman_filter.processNoiseCov = diagonal(1.0, 0.01, repeats=(3, 4))
        # set initial state value
        velocity_components = self.kalman_filter.statePost[4:].reshape(-1)
        self.kalman_filter.statePost = np.array([*state_center, *velocity_components], dtype=np.float32).reshape(-1, 1)
