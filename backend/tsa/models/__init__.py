from tsa import enums
from tsa.config import config

from . import detection, tracking
from .abstract import PredictableModel, TrackableModel

DETECTION_MODEL_MAPPING = {
    enums.DetectionModels.efficientdet_d5_adv_prop: detection.EfficientDetD5AdvPropAA,
    enums.DetectionModels.efficientdet_d6: detection.EfficientDetD6,
}

TRACKING_MODEL_MAPPING = {
    enums.TrackingModel.simple_sort: tracking.SimpleSORT,
    enums.TrackingModel.deep_sort: tracking.DeepSORT,
}


def init_detection_model(model_name: enums.DetectionModels) -> abstract.PredictableModel:
    model = DETECTION_MODEL_MAPPING[model_name]
    return model(
        config.ED_MAX_OUTPUTS,
        config.ED_IOU_THRESHOLD,
        config.ED_SCORE_THRESHOLD,
        config.ED_NSM_SIGMA,
        config.ED_BATCH_SIZE,
    )


def init_tracking_model(model_name: enums.TrackingModel) -> abstract.TrackableModel:
    if model_name == enums.TrackingModel.deep_sort:
        return tracking.DeepSORT(
            config.DEEP_SORT_MIN_UPDATES,
            config.DEEP_SORT_MAX_AGE,
            config.DEEP_SORT_IOU_THRESHOLD,
            config.DEEP_SORT_MAX_COSINE_DISTANCE,
            config.DEEP_SORT_MAX_MEMORY_SIZE,
        )
    return tracking.SimpleSORT(
        config.SORT_MIN_UPDATES,
        config.SORT_MAX_AGE,
        config.SORT_IOU_THRESHOLD,
    )


__all__ = ["PredictableModel", "TrackableModel", "init_detection_model", "init_tracking_model"]
