import os
import unittest
from unittest.mock import patch

import tensorflow
import logging

from testModel import detect_fruit, load_model


class TestModel(unittest.TestCase):
    @patch('tensorflow.keras.models.load_model')
    def setUp(self, mock_load_model):
        self.img_file_path = './src/pixelApple.jpg'
        self.model = None
        if os.path.exists(self.img_file_path):
            self.model = tensorflow.keras.models.load_model(
                os.path.join(os.path.abspath(os.path.join('output_files', 'model')), "model.tf"))

    def test_detect_fruit(self):
        logger = logging.getLogger(__name__)

        if self.model is not None:
            logger.warning("\nUsing the actual model for testing...")
            probabilities, class_index, class_label = detect_fruit(self.img_file_path)

            logger.warning(f"Probabilities: {probabilities}")
            logger.warning(f"class_index: {class_index}")
            logger.warning(f"class_label: {class_label}")

    @patch('tensorflow.keras.models.load_model')
    def test_load_model(self, mock_load_model):
        with patch('src.testModel.os.path.isdir') as mock_is_dir:
            mock_is_dir.return_value = True
            load_model()
        mock_load_model.assert_called_once()

if __name__ == '__main__':
    unittest.main()