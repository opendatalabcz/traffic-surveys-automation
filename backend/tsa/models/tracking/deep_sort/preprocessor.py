import tensorflow as tf

from tsa.tf_utils import optional_resize_with_pad


def _frame_to_boxes(input_data):
    frame, frame_detections = input_data

    def transformation():
        return tf.map_fn(
            lambda bbox: tf.RaggedTensor.from_tensor(
                optional_resize_with_pad(frame[bbox[1] : bbox[3], bbox[0] : bbox[2]], 32, 32)
            ),
            frame_detections,
            infer_shape=False,
            fn_output_signature=tf.RaggedTensorSpec((None, None, 3), dtype=tf.uint8, ragged_rank=1),
        )

    def empty_tensor():
        return tf.ragged.constant((), dtype=tf.uint8, ragged_rank=2, inner_shape=(3,))

    return tf.cond(tf.greater(tf.shape(frame_detections)[0], 0), true_fn=transformation, false_fn=empty_tensor)


def frame_detections_to_crops(frames, detections):
    return tf.map_fn(
        _frame_to_boxes,
        (frames, detections),
        fn_output_signature=tf.RaggedTensorSpec((None, None, None, 3), dtype=tf.uint8, ragged_rank=2),
    )
