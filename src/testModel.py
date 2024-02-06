import os
from PIL import Image
import numpy as np

import tensorflow as tf

label_file = 'labels.txt'
train_dir = './data/Training'
saved_files = './output_files'

if not os.path.exists(saved_files):
    os.makedirs(saved_files)

    labels = os.listdir(train_dir)

def test_model(path: str):
    # Load the model once, outside your function
    name = 'model'
    model_out_dir = os.path.join(saved_files, name)
    if not os.path.exists(model_out_dir):
        print("No saved model found in: " + model_out_dir)
        exit(0)
    model = tf.keras.models.load_model(os.path.join(model_out_dir, "model.tf"))

    print("Testing model...")
    image = Image.open(path).resize((100, 100))
    data = np.array([np.asarray(image)], dtype=int)
    y_pred = model.predict(data, 1)
    print("Prediction probabilities: " + str(y_pred))
    print("Predicted class index: " + str(y_pred.argmax(axis=-1)))
    print("Predicted class label: " + labels[y_pred.argmax(axis=-1)[0]])
