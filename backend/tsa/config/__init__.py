from pathlib import Path
from typing import Any, Dict

from konfetti import Konfig

CONFIG_DIR = Path(__file__).parent

CONFIGURABLE_VARIABLES = {
    "VIDEO_FRAME_RATE": int,
    "VIDEO_MAX_FRAMES": int,
    "VIDEO_SHOW_CLASS": bool,
    "DEEP_SORT_MIN_UPDATES": int,
    "DEEP_SORT_MAX_AGE": int,
    "DEEP_SORT_IOU_THRESHOLD": float,
    "DEEP_SORT_MAX_COSINE_DISTANCE": float,
    "DEEP_SORT_MAX_MEMORY_SIZE": int,
    "ED_MAX_OUTPUTS": int,
    "ED_IOU_THRESHOLD": float,
    "ED_SCORE_THRESHOLD": float,
    "ED_NSM_SIGMA": float,
    "ED_BATCH_SIZE": int,
    "SORT_MIN_UPDATES": int,
    "SORT_MAX_AGE": int,
    "SORT_IOU_THRESHOLD": float,
    "INTERPOLATION_POLYNOMIAL_DEGREE": int,
    "INTERPOLATION_CURVE_POINTS": int,
    "VISUALIZATION_MIN_PATH_LENGTH": float,
    "VISUALIZATION_N_CLUSTERS": int,
}

config = Konfig.from_object("tsa.config.base")

config.extend_with_json(CONFIG_DIR / "efficientdet.config.json")
config.extend_with_json(CONFIG_DIR / "sort.config.json")
config.extend_with_json(CONFIG_DIR / "deep_sort.config.json")


def config_to_dict() -> Dict[str, Any]:
    return {c: config.__getattr__(c) for c in CONFIGURABLE_VARIABLES.keys()}
