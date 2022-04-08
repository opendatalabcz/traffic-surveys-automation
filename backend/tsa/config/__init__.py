from pathlib import Path
from typing import Any, Dict

from konfetti import Konfig

CONFIG_DIR = Path(__file__).parent

CONFIGURABLE_VARIABLES = {
    "VIDEO_FRAME_RATE",
    "VIDEO_MAX_FRAMES",
    "VIDEO_SHOW_CLASS",
    "DEEP_SORT_MIN_UPDATES",
    "DEEP_SORT_MAX_AGE",
    "DEEP_SORT_IOU_THRESHOLD",
    "DEEP_SORT_MAX_COSINE_DISTANCE",
    "DEEP_SORT_MAX_MEMORY_SIZE",
    "ED_MAX_OUTPUTS",
    "ED_IOU_THRESHOLD",
    "ED_SCORE_THRESHOLD",
    "ED_NSM_SIGMA",
    "ED_BATCH_SIZE",
    "SORT_MIN_UPDATES",
    "SORT_MAX_AGE",
    "SORT_IOU_THRESHOLD",
    "INTERPOLATION_POLYNOMIAL_DEGREE",
    "INTERPOLATION_CURVE_POINTS",
    "VISUALIZATION_MIN_PATH_LENGTH",
    "VISUALIZATION_N_CLUSTERS",
}

config = Konfig.from_object("tsa.config.base")

config.extend_with_json(CONFIG_DIR / "efficientdet.config.json")
config.extend_with_json(CONFIG_DIR / "sort.config.json")
config.extend_with_json(CONFIG_DIR / "deep_sort.config.json")


def config_to_dict() -> Dict[str, Any]:
    return {c: config.__getattr__(c) for c in CONFIGURABLE_VARIABLES}
