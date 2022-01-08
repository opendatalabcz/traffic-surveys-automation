import numpy as np
from numpy.testing import assert_almost_equal, assert_array_equal

from tsa.cv2.kalman_filter import KalmanFilter


def test_kalman_filter_initialization():
    initial_position = np.array([10., 10., 15., 15.])
    tracker = KalmanFilter(initial_position)
    # check if all the tracker variables were initialized properly
    assert_array_equal(tracker.kalman_filter.measurementMatrix, np.eye(4, 10))
    assert_array_equal(tracker.kalman_filter.measurementNoiseCov, np.diag([1., 1., 10., 10.]))
    assert_almost_equal(tracker.kalman_filter.processNoiseCov, np.diag([1., 1., 1., 1., 0.01, 0.01, 0.01, 0.01]))
    assert_almost_equal(tracker.kalman_filter.statePost, np.array([12.5, 12.5, 1., 5., 0., 0., 0., 0.]).reshape(-1, 1))
    assert_almost_equal(
        tracker.kalman_filter.errorCovPost, np.diag([0.25, 0.25, 1e-4, 0.25, 0.09765625, 0.09765625, 1e-25, 0.09765625]),
    )


def test_kalman_filter_prediction():
    initial_position = np.array([10., 10., 15., 15.])
    kalman_filter = KalmanFilter(initial_position)
    next_position = kalman_filter.predict()
    assert_almost_equal(next_position, initial_position)
