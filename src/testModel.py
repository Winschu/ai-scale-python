import os
from PIL import Image, UnidentifiedImageError
import tensorflow
import numpy as tnp
from typing import List, Tuple

label_file = './labels.txt'
train_dir = './data/Training'
saved_files = './output_files'

with open(label_file, "r") as f:
    labels = [x.strip() for x in f.readlines()]

model = None

def load_model():
    global model
    model_out_dir = os.path.abspath(os.path.join(saved_files, 'model'))

    if not os.path.isdir(model_out_dir):
        print("No saved model directory found in: " + model_out_dir)
        exit(0)
    else:
        print("Model directory: " + model_out_dir)

    model = tensorflow.keras.models.load_model(os.path.join(model_out_dir, "model.tf"), compile=False)

def detect_fruit(image_path: str) -> Tuple[List[float], int, str]:
    global model
    if model is None:
        print("Model is not loaded. Loading model...")
        load_model()  # call the load_model function here

    print("Testing model...")
    try:
        img = Image.open(image_path).resize((100, 100))
    except UnidentifiedImageError:
        print("Cannot identify image file. The image file might be corrupted or it's not a valid image file.")
        return [0] * len(labels), -1, "Error"


    img = tensorflow.keras.preprocessing.image.img_to_array(img)  # Change here

    # Add an extra dimension for batch size
    img = tnp.expand_dims(img, axis=0)

    y_pred = model.predict(img, 1)

    # Convert probabilities into percentage and round to 2 decimal places
    probabilities = (y_pred[0] * 100).round(2).tolist()
    predicted_class_index = int(tnp.argmax(y_pred, axis=-1))  # Store in a variable

    print("Prediction probabilities: " + str(probabilities) + "%")
    print("Predicted class index: " + str(predicted_class_index))
    print("Predicted class label: " + labels[predicted_class_index])  # Use the variable here

    predictedClass = str(labels[predicted_class_index])

    # Return prediction probabilities, predicted class index, and predicted class label
    return probabilities, predicted_class_index, predictedClass

detect_fruit("./pixelApple.jpg")