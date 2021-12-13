import numpy as np
from numpy.testing import assert_almost_equal, assert_array_equal

from tsa.cv2.kalman_tracker import KalmanTracker


def test_kalman_tracker_initialization():
    initial_position = np.array([10., 10., 15., 15.])
    tracker = KalmanTracker(initial_position)
    # check if all the tracker variables were initialized properly
    assert_array_equal(tracker.kalman_filter.measurementMatrix, np.eye(4, 7))
    assert_array_equal(tracker.kalman_filter.measurementNoiseCov, np.diag([1., 1., 10., 10.]))
    assert_array_equal(tracker.kalman_filter.errorCovPost, np.diag([10., 10., 10., 10_000., 10_000., 10_000., 10_000.]))
    assert_almost_equal(tracker.kalman_filter.processNoiseCov, np.diag([1., 1., 1., 0.01, 0.01, 0.01, 0.01]))
    assert_almost_equal(tracker.kalman_filter.statePost, np.array([12.5, 12.5, 25., 1., 0., 0., 0.]).reshape(-1, 1))
    # check if prediction works
    assert_almost_equal(tracker.predict(), initial_position)
