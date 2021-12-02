from uuid import uuid4

import cv2
import numpy as np

from tsa.bbox import BBox

KF_DIMENSION_PARAMS = 7
KF_MEASUREMENT_PARAMS = 4


class KalmanTracker:
    def __init__(self):
        self.id = uuid4()
        self.kalman_filter = cv2.KalmanFilter(dynamParams=KF_DIMENSION_PARAMS, measureParams=KF_MEASUREMENT_PARAMS)
        # correct the kalman filter initial values
        self.kalman_filter.measurementMatrix = np.eye(KF_MEASUREMENT_PARAMS, KF_DIMENSION_PARAMS, dtype=np.float32)

    def update(self, bbox: BBox):
        correction_state_array = bbox.to_numpy_center().astype(np.float32)
        self.kalman_filter.correct(correction_state_array)

    def predict(self) -> BBox:
        prediction = self.kalman_filter.predict()
        return BBox.from_numpy_center(prediction[:4])
