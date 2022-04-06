from enum import Enum


class DetectionModels(Enum):
    efficientdet_d6 = "efficientdet_d6"
    efficientdet_d5_adv_prop = "efficientdet_d5_adv_prop"


class TrackingModel(Enum):
    simple_sort = "simple_sort"
    deep_sort = "deep_sort"


class SourceFileStatus(Enum):
    new = "new"
    processing = "processing"
    processed = "processed"
    deleted = "deleted"


class TaskStatus(Enum):
    created = "created"
    processing = "processing"
    completed = "completed"
    failed = "failed"
