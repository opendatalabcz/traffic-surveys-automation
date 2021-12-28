from typing import List, Optional

import numpy as np
import tensorflow as tf

from tsa.typing import IMAGE_SHAPE


def center_to_bbox(center):
    center_x, center_y, area, ratio = center
    width = np.sqrt(area * ratio)
    height = area / width
    x1, x2 = center_x - width / 2.0, center_x + width / 2.0
    y1, y2 = center_y - height / 2.0, center_y + height / 2.0
    return np.array([x1, y1, x2, y2], dtype=np.float32), (width, height)


def bbox_to_center(bbox):
    x1, y1, x2, y2 = bbox
    width, height = x2 - x1, y2 - y1
    center_x, center_y = x1 + width / 2.0, y1 + height / 2.0
    area, ratio = width * height, width / height
    return np.array([center_x, center_y, area, ratio], dtype=np.float32)


class BBox:
    """Representation of a single bounding box.

    This class helps with converting bounding boxes to different formats and types. Internally, a bounding box is
    represented by top-left and bottom-right positions. Available methods allow to convert it to different formats.
    """

    def __init__(self, bbox, size: Optional[IMAGE_SHAPE] = None):
        """Initialize a bounding box.

        @param bbox array of size 4 with top-left and bottom-right coordinates of the bbox
        @param size size of the image the bounding box belongs to, it is use for scaling the bbox up to the original
        size
        """
        # multiplication matrix for adjusting bbox to the provided size
        self.size = (
            tf.constant([*size, *size], dtype=tf.float32)
            if size is not None
            else tf.constant([1, 1, 1, 1], dtype=tf.float32)
        )
        self.bbox = bbox

    @classmethod
    def from_tensor_list(cls, tensor, image_height: Optional[int], image_width: Optional[int]) -> List["BBox"]:
        """Initialize a list of bboxes with tensor containing 4 rows (x1, y1, x2, y2)."""
        size = (image_width, image_height) if image_height and image_width else None
        return list(map(lambda bbox: cls(bbox, size), tensor))

    @classmethod
    def from_numpy_center(cls, center) -> "BBox":
        bbox, size = center_to_bbox(center)
        return cls(tf.constant(bbox, dtype=tf.float32))

    @property
    def scaled_bbox(self):
        return self.bbox * self.size

    def to_numpy_center(self):
        """Returns scaled numpy array of (centerX, centerY, area, aspect ratio)."""
        return bbox_to_center(self.scaled_bbox.numpy())

    def to_rectangle(self):
        """Returns scaled numpy array if (leftX, leftY), (rightX, rightY)."""
        return self.scaled_bbox.numpy().astype(np.int32)
