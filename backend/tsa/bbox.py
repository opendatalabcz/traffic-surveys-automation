from typing import Tuple

import numpy as np

from tsa import typing


def center_to_bbox(center: typing.BBOX_CENTER) -> Tuple[typing.BBOX_COORDINATES, typing.IMAGE_SHAPE]:
    center_x, center_y, ratio, height = center
    width = ratio * height
    x1, x2 = center_x - width / 2.0, center_x + width / 2.0
    y1, y2 = center_y - height / 2.0, center_y + height / 2.0
    return np.array([x1, y1, x2, y2], dtype=np.float32), (width, height)


def bbox_to_center(bbox: typing.BBOX_COORDINATES) -> typing.BBOX_CENTER:
    x1, y1, x2, y2 = bbox
    width, height = x2 - x1, y2 - y1
    center_x, center_y, ratio = x1 + width / 2.0, y1 + height / 2.0, width / height
    return np.array([center_x, center_y, ratio, height], dtype=np.float32)
