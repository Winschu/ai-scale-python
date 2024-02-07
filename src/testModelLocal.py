import os
from PIL import Image
import numpy as np

from tensorflow.keras.models import load_model

import tensorflow as tf
print(tf.__version__)

use_label_file = False  # set this to true if you want load the label names from a file; uses the label_file defined below; the file should contain the names of the used labels, each label on a separate line
label_file = 'labels.txt'
base_dir = './data/'  # relative path to the Fruit-Images-Dataset folder
train_dir = os.path.join(base_dir, 'Training')
test_dir = os.path.join(base_dir, 'Test')
saved_files = os.path.join(os.getcwd(), 'output_files')

if not os.path.exists(saved_files):
    os.makedirs(saved_files)

if use_label_file:
    with open(label_file, "r") as f:
        labels = [x.strip() for x in f.readlines()]
else:
    labels = os.listdir(train_dir)

# Load the model once, outside your function
name = 'model'
model_out_dir = os.path.join(saved_files, name)

if not os.path.exists(model_out_dir):
    print("No saved model found in: " + model_out_dir)
    exit(0)

complete_path = os.path.join(model_out_dir, "model.tf")

print(f"Complete path: {complete_path}")

try:
    model = load_model(os.path.join(model_out_dir, "model.tf"))
except Exception as e:
    print(f"Failed to load the model. Error: {e}")
    raise


def test_model():
    print("Testing model...")
    image = Image.open(test_dir + '/appleSideTest.jpg').resize((100, 100))

    if image:
        print("Image is loaded successfully.")
        image.show()  # This line will display the image

        # Try converting the image to numpy array
        try:
            np_image = np.array(image, dtype=int)

            # Check if the conversion was successful
            if np_image is not None:
                print("Conversion to numpy array successful.")
                print("Image as numpy array:", np_image)

            else:
                print("Failed to convert image to numpy array.")
        except TypeError as e:
            print(f"A TypeError occurred during conversion to numpy array: {str(e)}")
        except ValueError as e:
            print(f"A ValueError occurred during conversion to numpy array: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred during conversion to numpy array: {str(e)}")
    else:
        print("Image failed to load.")

    data = np.array([np.asarray(image)], dtype=int)
    y_pred = model.predict(data, 1)
    print("Prediction probabilities: " + str(y_pred))
    print("Predicted class index: " + str(y_pred.argmax(axis=-1)))
    print("Predicted class label: " + labels[y_pred.argmax(axis=-1)[0]])


test_model()
