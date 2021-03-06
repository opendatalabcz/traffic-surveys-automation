import tensorflow as tf


def optional_resize_with_crop_or_pad(image, min_height: int, min_width: int, max_height: int, max_width: int, **kwargs):
    """Resize and pad or crop an image only when it's original shape is outside the predefined shapes.

    Otherwise, keep the original dimension.
    """
    image_shape = tf.shape(image)
    target_height, target_with = (
        tf.minimum(max_height, tf.maximum(min_height, image_shape[0])),
        tf.minimum(max_width, tf.maximum(min_width, image_shape[1])),
    )

    resized_image = tf.image.resize_with_crop_or_pad(image, target_height, target_with, **kwargs)
    resized_image = tf.cast(resized_image, image.dtype)

    return resized_image
