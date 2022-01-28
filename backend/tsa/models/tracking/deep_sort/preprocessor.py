import tensorflow as tf

from tsa.tf_utils import optional_resize_with_pad


def _frame_to_boxes(input_data):
    frame, frame_detections = input_data

    return tf.map_fn(
        lambda bbox: tf.RaggedTensor.from_tensor(
            optional_resize_with_pad(frame[bbox[1]: bbox[3], bbox[0]: bbox[2]], 32, 32)
        ),
        frame_detections,
        infer_shape=False,
        fn_output_signature=tf.RaggedTensorSpec((None, None, 3), dtype=tf.uint8, ragged_rank=1),
    )


def frame_detections_to_crops(frames, detections):
    return tf.map_fn(
        _frame_to_boxes,
        (frames, detections),
        fn_output_signature=tf.RaggedTensorSpec((None, None, None, 3), dtype=tf.uint8, ragged_rank=2),
    )
