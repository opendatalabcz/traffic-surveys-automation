import numpy as np
from numpy.testing import assert_array_almost_equal

from tsa.bbox import BBox
from tsa.models.tracking.sort import SORT


def test_sort():
    sort = SORT(1, 3, 0.7)
    step_1 = [BBox.from_numpy_center(np.array([120, 70, 2, 100]))]
    tracking, _, _ = sort.track(step_1)
    assert not tracking
    step_2 = [BBox.from_numpy_center(np.array([130, 70, 2, 100]))]
    tracking, _, _ = sort.track(step_2)
    assert_array_almost_equal(tracking[0], np.array([29.93, 20., 229.93, 120.]), decimal=2)
