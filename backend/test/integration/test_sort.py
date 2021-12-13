import numpy as np
from numpy.testing import assert_array_almost_equal

from tsa.bbox import BBox
from tsa.models.tracking.sort import SORT


def test_sort():
    sort = SORT()
    step_1 = [BBox.from_numpy_center(np.array([100.0, 50.0, 400.0, 1.0]))]
    tracking, _ = sort.track(step_1)
    assert_array_almost_equal(tracking[0], np.array([90.0, 40.0, 110.0, 60.0]))
    step_2 = [BBox.from_numpy_center(np.array([105.0, 55.0, 400.0, 1.0]))]
    tracking, _ = sort.track(step_2)
    assert_array_almost_equal(tracking[0], np.array([94.58, 44.58, 114.58, 64.58]), decimal=2)
