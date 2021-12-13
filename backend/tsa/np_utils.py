import numpy as np


def diagonal(*values, repeats=None, dtype=np.float32):
    if repeats is None:
        return np.diag(values).astype(dtype)
    return np.diag(np.repeat(values, repeats)).astype(dtype)
