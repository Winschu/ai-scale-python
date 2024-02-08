import os
from PIL import Image
import numpy as np

import tensorflow as tf

label_file = './src/labels.txt'
train_dir = './data/Training'
saved_files = './src/output_files'

with open(label_file, "r") as f:
    labels = [x.strip() for x in f.readlines()]


def test_model(image_path: str):
    # Load the model once, outside your function
    model_out_dir = os.path.abspath(os.path.join(saved_files, 'model'))

    if not os.path.isdir(model_out_dir):
        print("No saved model directory found in: " + model_out_dir)
        exit(0)
    else:
        print("Model directory: " + model_out_dir)

    model = tf.keras.models.load_model(os.path.join(model_out_dir, "model.tf"))

    print("Testing model...")
    image = Image.open(image_path).resize((100, 100))
    data = np.array([np.asarray(image)], dtype=int)
    y_pred = model.predict(data, 1)
    print("Prediction probabilities: " + str(y_pred))
    print("Predicted class index: " + str(y_pred.argmax(axis=-1)))
    print("Predicted class label: " + labels[y_pred.argmax(axis=-1)[0]])
