import unittest
import base64
import json
from unittest.mock import patch
from flask import Flask
from src.image_processing import upload_image, handle_file_size_too_large, is_valid_base64, request


class TestHandleFileSizeTooLarge(unittest.TestCase):
    @patch.object(request, 'content_length', 1000)
    @patch.object(request, 'max_content_length', 500)
    def test_handle_file_size_too_large(self):
        res = handle_file_size_too_large(Exception())
        self.assertEqual(res, ("Die Datei ist zu groß. Sie überschreitet das Limit um 500 Bytes.", 413))


class TestIsValidBase64(unittest.TestCase):
    def test_is_valid_base64(self):
        # Generating a sample base64 string
        sample_string = base64.b64encode(b"Test string")
        self.assertTrue(is_valid_base64(sample_string.decode('utf-8')))

        # Input with invalid characters
        invalid_input = "@@@@"
        self.assertFalse(is_valid_base64(invalid_input))

        # Input with valid characters but length not multiple of 4
        invalid_input = "abc"
        self.assertFalse(is_valid_base64(invalid_input))

class TestUploadImage(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

        self.client = self.app.test_client()
        self.app.route('/upload', methods=['POST'])(upload_image)

    @patch('src.your_script.detect_fruit', return_value=(0.9, 1, "Apple"))
    def test_upload_image(self, detect_fruit):
        with self.app.app_context():
            string_binary = b"test image"
            filename = base64.b64encode(string_binary).decode()

            response = self.client.post('/upload', data=json.dumps({
                'image_data': f'data:image/jpg;base64,{filename}',
                'weight': '5.5'
            }), content_type='application/json')

            self.assertEqual(response.status_code, 200)

            json_data = response.get_json()

            self.assertEqual(json_data['status'], 'success')
            self.assertEqual(json_data['weight'], '5.5')
            self.assertEqual(json_data['prediction']['probabilities'], 0.9)
            self.assertEqual(json_data['prediction']['class_index'], 1)
            self.assertEqual(json_data['prediction']['class_label'], "Apple")

if __name__ == "__main__":
    unittest.main()