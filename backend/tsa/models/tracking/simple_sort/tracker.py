from uuid import uuid4

from tsa import typing, bbox
from tsa.cv2.kalman_filter import KalmanFilter


class Tracker:
    def __init__(self, initial_position: typing.BBOX_COORDINATES, min_updates: int, max_age: int):
        self.id, self.updates, self.predictions, self.time_since_update = uuid4(), 0, 0, 0
        self.min_updates, self.max_time_since_update = min_updates, max_age
        self.kalman_filter = KalmanFilter(bbox.bbox_to_center(initial_position))

    @property
    def state(self) -> typing.BBOX_COORDINATES:
        bbox_prediction, _ = bbox.center_to_bbox(self.kalman_filter.state)
        return bbox_prediction

    @property
    def is_active(self) -> bool:
        return self.updates >= self.min_updates

    @property
    def is_deleted(self) -> bool:
        return (
            self.time_since_update > self.max_time_since_update or
            (not self.is_active and self.updates != self.predictions)
        )

    def update(self, new_position: typing.BBOX_COORDINATES):
        self.updates += 1
        self.time_since_update = 0

        self.kalman_filter.update(bbox.bbox_to_center(new_position))

    def predict(self) -> typing.BBOX_COORDINATES:
        self.predictions += 1

        prediction = self.kalman_filter.predict()
        bbox_prediction, _ = bbox.center_to_bbox(prediction)
        return bbox_prediction
