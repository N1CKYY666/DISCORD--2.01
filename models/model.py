
"""Classify images using a trained Keras model."""

import numpy as np
from keras.models import load_model
from PIL import Image, ImageOps


def get_class(model_path, labels, image_path):
    """Classify an image and return its confidence level."""

    # Display NumPy values without scientific notation.
    np.set_printoptions(suppress=True)

    # Load the trained model without compiling it.
    model = load_model(model_path, compile=False)

    # Read the classification labels.
    with open(labels, "r", encoding="utf-8") as label_file:
        class_names = label_file.readlines()

    # Create an array to store the processed image.
    data = np.ndarray(
        shape=(1, 224, 224, 3),
        dtype=np.float32
    )

    # Open the image and convert it to RGB.
    image = Image.open(image_path).convert("RGB")

    # Resize and crop the image to match the model input.
    size = (224, 224)
    image = ImageOps.fit(
        image,
        size,
        Image.Resampling.LANCZOS
    )

    # Convert the image into a NumPy array.
    image_array = np.asarray(image)

    # Normalize pixel values to the range [-1, 1].
    normalized_image_array = (
        image_array.astype(np.float32) / 127.5
    ) - 1

    data[0] = normalized_image_array

    # Predict the image classification.
    prediction = model.predict(data, verbose=0)

    # Find the class with the highest probability.
    index = np.argmax(prediction)

    class_name = class_names[index][2:].strip()
    confidence_score = prediction[0][index]

    # Determine the confidence level of the prediction.
    if confidence_score >= 0.90:
        message = "High confidence"
    elif confidence_score >= 0.70:
        message = "Moderate confidence"
    else:
        message = "Low confidence"

    return class_name, confidence_score, message
