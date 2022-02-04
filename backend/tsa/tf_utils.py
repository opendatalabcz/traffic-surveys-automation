import tensorflow as tf


def optional_resize_with_pad(image, height: int, width: int, **kwargs):
    """Resize and pad an image only when it's original shape is smaller than the target shape.

    Otherwise, keep the original dimension.
    """
    image_shape = tf.shape(image)
    target_height, target_with = tf.maximum(height, image_shape[0]), tf.maximum(width, image_shape[1])

    resized_image = tf.image.resize_with_pad(image, target_height, target_with, **kwargs)
    resized_image = tf.cast(resized_image, image.dtype)

    return resized_image
