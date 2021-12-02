import numpy as np
import tensorflow as tf

from tsa.bbox import BBox


def test_bbox_from_tensor():
    # let's have a tensor with two bboxes
    input_tensor = tf.constant([[0.5, 0.5, 0.6, 0.6], [0.7, 0.1, 0.8, 0.2]])
    # when we convert it into a list of BBox classes
    bbox_list = BBox.from_tensor_list(input_tensor, 720, 1280)
    # the list is 2 items long
    assert len(bbox_list) == 2
    # the convert methods return the expected values
    assert bbox_list[0].to_rectangle() == ((640, 360), (768, 432))
    assert bbox_list[0].to_numpy_center() == np.array([704, 396, 921_600, 1.7])
