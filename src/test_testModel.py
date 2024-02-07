import os
import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from PIL import Image
import tensorflow as tf


class TestModelTest(unittest.TestCase):
    @patch('tensorflow.keras.models.load_model')
    @patch('os.path.exists')
    @patch('os.path.join')
    @patch('PIL.Image.Image.resize')
    @patch('PIL.Image.open')
    def test_test_model(self, mock_open, mock_resize, mock_join, mock_exists, mock_load_model):

        current_dir = os.path.dirname(os.path.abspath(__file__))  # get current directory
        image_path = os.path.join(current_dir, 'test_image.jpg')  # append file name

        mock_exists.return_value = True

        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([[0.1, 0.9]])
        mock_load_model.return_value = mock_model

        mock_image = MagicMock(spec=Image.Image)
        mock_open.return_value = mock_image
        mock_image.resize.return_value = mock_image

        mock_join.return_value = './output_files/model/model.tf'

        # You may need to adjust the labels accordingly
        labels = ["label_0", "label_1"]

        # Act
        from testModel import test_model  # assuming that your function resides in test_script.py
        test_model(image_path)

        # Assert
        mock_open.assert_called_once_with(image_path)
        mock_image.resize.assert_called_once_with((100, 100))
        mock_model.predict.assert_called_once()


if __name__ == "__main__":
    unittest.main()
