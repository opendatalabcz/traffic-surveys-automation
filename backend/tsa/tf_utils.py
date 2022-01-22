import tensorflow as tf


def conditional_concat(tensor_a, tensor_b, axis):
    """Concatenate two tensors if `tensor_b` has the same rank as `tensor_b`."""
    if tensor_b.shape[axis] == 0:
        return tensor_a

    return tf.concat((tensor_a, tensor_b), axis=axis)
