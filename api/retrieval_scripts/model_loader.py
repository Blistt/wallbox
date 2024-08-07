'''
This function loads the VGG19 model from the keras library, modifies it so that it 
returns the feature maps of the layers, and returns the model.
'''

import tensorflow as tf

def load_model(model_name='VGG19'):

    visual_model = None

    if model_name=='VGG19':
        model = tf.keras.applications.VGG19(
        include_top=True,
        weights="imagenet",
        input_tensor=None,
        input_shape=None,
        pooling=None,
        classes=1000,
        classifier_activation="softmax",)

        layer_outputs = [layer.output for layer in model.layers[1:-1]]  # Identifies layer outputs
        # Creates a model that will return the layer feature maps as outputs for a given image
        visual_model = tf.keras.models.Model(inputs = model.input, outputs = layer_outputs) 

    if visual_model is None:
        raise ValueError('Invalid model name')

    return visual_model