import hashlib
from typing import Union

import numpy as np


def diagonal(*values, repeats=None, dtype=np.float32):
    if repeats is None:
        return np.diag(values).astype(dtype)
    return np.diag(np.repeat(values, repeats)).astype(dtype)


def iou_batch(bb_test, bb_gt):
    """Compute an intersection over union on a batch of bounding boxes.

    Adopted from https://github.com/abewley/sort/blob/bce9f0d1fc8fb5f45bf7084130248561a3d42f31/sort.py#L47.
    The LICENCE is the same as of our project, stated at the root level of the repository.
    """
    bb_gt = np.expand_dims(bb_gt, 0)
    bb_test = np.expand_dims(bb_test, 1)

    xx1 = np.maximum(bb_test[..., 0], bb_gt[..., 0])
    yy1 = np.maximum(bb_test[..., 1], bb_gt[..., 1])
    xx2 = np.minimum(bb_test[..., 2], bb_gt[..., 2])
    yy2 = np.minimum(bb_test[..., 3], bb_gt[..., 3])
    w = np.maximum(0.0, xx2 - xx1)
    h = np.maximum(0.0, yy2 - yy1)
    wh = w * h
    o = wh / (
        (bb_test[..., 2] - bb_test[..., 0]) * (bb_test[..., 3] - bb_test[..., 1])
        + (bb_gt[..., 2] - bb_gt[..., 0]) * (bb_gt[..., 3] - bb_gt[..., 1])
        - wh
    )
    return o


class RandomGenerator:
    def __init__(self, seed: Union[int, str]):
        if isinstance(seed, str):
            seed = int(hashlib.sha1(seed.encode("utf-8")).hexdigest(), 16)

        self._random_generator = np.random.default_rng(seed=seed)

    def colors(self, count: int = 1):
        return self._random_generator.integers(0, 256, size=(count, 3)).tolist()
