import tensorflow as tf

from tsa.bbox import BBox
from tsa.datasets import VideoFramesDataset
from tsa.models.tracking import DeepSORT


def test_deep_sort():
    video = VideoFramesDataset("/Users/ondrejpudis/traffic_survey_automation/datasets/jackson-hole_20210507_1.mp4")
    tracking_model = DeepSORT(0, 3, 0.5, 0.4, 100)

    def track(bboxes):
        frame = next(video.frames)
        tracking_model.set_frame(frame)
        matched_boxes, _, _ = tracking_model.track(bboxes)
        return matched_boxes

    boxes = track(
        [
            BBox(tf.constant([735.8133, 559.89923, 1022.4664, 718.304], dtype=tf.float32)),
            BBox(tf.constant([687.3946, 413.50153, 884.4643, 489.71753], dtype=tf.float32)),
            BBox(tf.constant([576.85657, 374.93683, 724.72485, 435.9701], dtype=tf.float32)),
        ]
    )
    assert all(box is None for box in boxes)

    boxes = track(
        [
            BBox(tf.constant([735.7361, 559.5111, 1023.9169, 718.208], dtype=tf.float32)),
            BBox(tf.constant([712.24066, 414.1615, 915.1154, 491.7367], dtype=tf.float32)),
            BBox(tf.constant([557.99896, 373.97186, 703.7801, 435.44177], dtype=tf.float32)),
        ]
    )
    assert all(box is not None for box in boxes)
