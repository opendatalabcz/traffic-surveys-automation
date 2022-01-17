from typing import Optional

import numpy as np

from tsa import bbox as bbox_functions


class Detection(object):
    """
    This class represents a bounding box detection in a single image.

    Parameters
    ----------
    bbox : array_like
        Bounding box in format `(top_left_x, top_left_y, bottom_right_x, bottom_right_y)`.
    feature : array_like
        A feature vector that describes the object contained in this image.

    Attributes
    ----------
    bbox : ndarray
        Bounding box in format `(top left x, top left y, bottom_right_x, bottom_right_y)`.
    feature : ndarray | NoneType
        A feature vector that describes the object contained in this image.

    """

    def __init__(self, bbox, feature: Optional):
        self.bbox = np.asarray(bbox, dtype=np.float32)
        self.feature = np.asarray(feature, dtype=np.float32) if feature is not None else None

    def to_xyah(self):
        """Convert bounding box to format `(center x, center y, aspect ratio,
        height)`, where the aspect ratio is `width / height`.
        """
        return bbox_functions.bbox_to_center(self.bbox)
