import numpy as np
import tensorflow as tf
from numpy.testing import assert_array_equal

from tsa.bbox import BBox


def test_bbox_from_tensor():
    # let's have a tensor with two bboxes
    input_tensor = tf.constant([[0.5, 0.5, 0.6, 0.6], [0.1, 0.7, 0.2, 0.8]])
    # when we convert it into a list of BBox classes
    bbox_list = BBox.from_tensor_list(input_tensor, 720, 1280)
    # the list is 2 items long
    assert len(bbox_list) == 2
    # the convert methods return the expected values
    assert_array_equal(bbox_list[0].to_rectangle(), np.array([640, 360, 768, 432]))
    assert_array_equal(bbox_list[0].to_numpy_center()[:2], np.array([704, 396]))
