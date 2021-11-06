from enum import Enum


class DetectionModelType(str, Enum):
    faster_rcnn = "tensorflow/faster_rcnn/resnet152_v1_1024x1024/1"
