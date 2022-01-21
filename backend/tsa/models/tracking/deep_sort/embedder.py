import tensorflow as tf


def mobilenet_embedder():
    """
    MobileNetEmbedder loads a MobileNetV2 pretrained on Imagenet1000, with classification layer removed,
    exposing the bottleneck layer, outputting a feature of size 1280.
    """
    original_inputs = tf.keras.layers.Input([None, None, 3], dtype=tf.float32, ragged=True)

    inputs, inputs_mask = original_inputs.to_tensor(), tf.sequence_mask(original_inputs.row_lengths())
    inputs = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)

    mobilenet = tf.keras.applications.mobilenet_v2.MobileNetV2(
        input_shape=(160, 160, 3), include_top=False, pooling="avg", weights="imagenet"
    )
    mobilenet_output = mobilenet(inputs, mask=inputs_mask)

    return tf.keras.Model(inputs=original_inputs, outputs=mobilenet_output)
