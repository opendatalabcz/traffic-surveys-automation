from typing import Generator, List, Optional, Tuple, TypeVar

import numpy as np
from numpy import typing as npt

# general typing
IMAGE_SHAPE = Tuple[int, int]  # in form of width, height

# numpy typing
NP_ARRAY = npt.ArrayLike
NP_FRAME = npt.NDArray[np.uint8]

# custom shapes typing
BBOX_COORDINATES = TypeVar("BBOX_COORDINATES")  # BBOX in form (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
BBOX_CENTER = TypeVar("BBOX_CENTER")  # BBOX in form (center_x, center_y, ratio, height)
MATCHED_BBOXES = NP_ARRAY
MATCHED_IDS = List[Optional[str]]

# objects
FRAME_GENERATOR = Generator[NP_FRAME, None, None]
