import numpy as np
from numpy.testing import assert_array_almost_equal

from tsa.models.tracking import SimpleSORT


def test_sort():
    sort = SimpleSORT(1, 3, 0.7)
    for tracking, _, _ in sort.track(np.array([[[20.,  20., 220., 120.]]])):
        assert not tracking
    for tracking, _, _ in sort.track(np.array([[[30., 20., 230., 120.]]])):
        assert_array_almost_equal(tracking[0], np.array([29.93, 20., 229.93, 120.]), decimal=2)
