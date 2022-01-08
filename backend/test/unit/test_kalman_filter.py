import numpy as np
from numpy.testing import assert_almost_equal, assert_array_equal

from tsa import bbox
from tsa.cv2.kalman_filter import KalmanFilter


def test_kalman_filter_initialization():
    def get_process_noise_cov(delta: float):
        return np.stack(
            [
                [delta ** 4 / 4, 0, 0, 0, delta ** 3 / 2, 0, 0, 0, delta ** 2 / 2, 0],
                [0, delta ** 4 / 4, 0, 0, 0, delta ** 3 / 2, 0, 0, 0, delta ** 2 / 2],
                [0, 0, delta ** 4 / 4, 0, 0, 0, delta ** 3 / 2, 0, 0, 0],
                [0, 0, 0, delta ** 4 / 4, 0, 0, 0, delta ** 3 / 2, 0, 0],
                [delta ** 3 / 2, 0, 0, 0, delta ** 2, 0, 0, 0, delta, 0],
                [0, delta ** 3 / 2, 0, 0, 0, delta ** 2, 0, 0, 0, delta],
                [0, 0, delta ** 3 / 2, 0, 0, 0, delta ** 2, 0, 0, 0],
                [0, 0, 0, delta ** 3 / 2, 0, 0, 0, delta ** 2, 0, 0],
                [delta ** 2 / 2, 0, 0, 0, delta, 0, 0, 0, 1, 0],
                [0, delta ** 2 / 2, 0, 0, 0, delta, 0, 0, 0, 1],
            ],
            axis=0,
        )

    def get_transition_matrix(delta: float):
        return np.stack(
            [
                [1, 0, 0, 0, delta, 0, 0, 0, 0.5 * delta ** 2, 0],
                [0, 1, 0, 0, 0, delta, 0, 0, 0, 0.5 * delta ** 2],
                [0, 0, 1, 0, 0, 0, delta, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, delta, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            ],
            axis=0,
        )

    initial_position = bbox.bbox_to_center(np.array([10., 10., 15., 15.]))
    tracker = KalmanFilter(initial_position)

    # check if all the tracker variables were initialized properly
    assert_array_equal(tracker.kalman_filter.measurementMatrix, np.eye(4, 10))
    assert_array_equal(tracker.kalman_filter.measurementNoiseCov, np.diag([9., 9., 25., 25.]))

    process_noise_cov = get_process_noise_cov(1.0) * 0.15
    assert np.all(np.abs(process_noise_cov - process_noise_cov.T) < 1e-8)
    assert_almost_equal(tracker.kalman_filter.processNoiseCov, process_noise_cov)

    transition_matrix = get_transition_matrix(1.0)
    assert_array_equal(tracker.kalman_filter.transitionMatrix, transition_matrix)

    assert_almost_equal(
        tracker.kalman_filter.statePost, np.array([12.5, 12.5, 1., 5., 0., 0., 0., 0., 0., 0.]).reshape(-1, 1)
    )
    assert_almost_equal(
        tracker.kalman_filter.errorCovPost,
        np.diag([100., 100., 100., 100., 1_000., 1_000., 1_000., 1_000., 1_000., 1_000.]),
    )


def test_kalman_filter_prediction():
    initial_position = np.array([10., 10., 15., 15.])
    kalman_filter = KalmanFilter(initial_position)
    next_position = kalman_filter.predict()
    assert_almost_equal(next_position, initial_position)
