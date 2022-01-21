import numpy as np
from numpy.testing import assert_almost_equal

from tsa import bbox


def test_bbox_to_center():
    # let's have a bounding box
    input_bounding_box = np.array([10, 30, 50, 80])
    # when we convert it into centered version
    centered_version = bbox.bbox_to_center(input_bounding_box)
    # the convert methods return the expected values
    assert_almost_equal(centered_version, np.array([30, 55, 0.8, 50]))


def test_center_to_bbox():
    # let's have a centered input
    input_center = np.array([30, 55, 0.8, 50])
    # when we convert it back to a bounding box version
    bounding_box, size = bbox.center_to_bbox(input_center)
    # the convert methods return the bbox and the size of that bbox
    assert_almost_equal(bounding_box, np.array([10, 30, 50, 80]))
    assert size == (40, 50)
