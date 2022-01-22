import tensorflow as tf

from tsa.datasets import VideoFramesDataset
from tsa.models.tracking import DeepSORT


def test_deep_sort():
    video = VideoFramesDataset("/Users/ondrejpudis/traffic_survey_automation/datasets/jackson-hole_20210507_1.mp4")
    tracking_model = DeepSORT(0, 3, 0.5, 0.4, 100)

    def track(bboxes):
        frame = next(video.frames)
        for matched_boxes, _, _ in tracking_model.track(bboxes, frames=tf.constant([frame], dtype=tf.uint8)):
            return matched_boxes

    boxes = track(
        tf.constant(
            [
                [
                    [735.8133, 559.89923, 1022.4664, 718.304],
                    [687.3946, 413.50153, 884.4643, 489.71753],
                    [576.85657, 374.93683, 724.72485, 435.9701],
                ]
            ]
        )
    )
    assert all(not box.all() for box in boxes)

    boxes = track(
        tf.constant(
            [
                [
                    [735.7361, 559.5111, 1023.9169, 718.208],
                    [712.24066, 414.1615, 915.1154, 491.7367],
                    [557.99896, 373.97186, 703.7801, 435.44177],
                ]
            ]
        )
    )
    assert all(box is not None for box in boxes)
