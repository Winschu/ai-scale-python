import os
from PIL import Image
import numpy as np

import tensorflow as tf

use_label_file = False  # set this to true if you want load the label names from a file; uses the label_file defined below; the file should contain the names of the used labels, each label on a separate line
label_file = 'labels.txt'
base_dir = '../../../..'  # relative path to the Fruit-Images-Dataset folder
train_dir = os.path.join(base_dir, 'Training')
#test_dir = os.path.join(base_dir, 'Test')
saved_files = os.getcwd() + '/output_files'  # root folder in which to save the the output files; the files will be under output_files/model_name

if not os.path.exists(saved_files):
    os.makedirs(saved_files)

    labels = os.listdir(train_dir)




def test_model(path: str):
    # Load the model once, outside your function
    name = 'fruit-360-model-gpu-30ep-100ba-reduced-labels'
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


test_model()
