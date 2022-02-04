from pathlib import Path

from konfetti import env

MODELS_PATH = env("MODELS_PATH", cast=Path)

VIDEO_FRAME_RATE = env("VIDEO_FRAME_RATE", default=15, cast=int)
VIDEO_MAX_FRAMES = env("VIDEO_MAX_FRAMES", default=None, cast=int)

INTERPOLATION_POLYNOMIAL_DEGREE = env("INTERPOLATION_POLYNOMIAL_DEGREE", default=3, cast=int)

VISUALIZATION_MIN_PATH_LENGTH = env("VISUALIZATION_MIN_PATH_LENGTH", default=150.0, cast=float)
VISUALIZATION_N_CLUSTERS = env("VISUALIZATION_N_CLUSTERS", default=12, cast=int)
