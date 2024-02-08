from flask import request, abort
import base64
import os
import re
import logging

from src.testModel import test_model

def handle_file_size_too_large(e):
    difference = request.content_length - request.max_content_length
    return f"Die Datei ist zu groß. Sie überschreitet das Limit um {difference} Bytes.", 413

def replace_spaces_with_plus(base64_string: str):
    return base64_string.replace(' ', '+')

def upload_image():
    # Receive the base64 encoded image
    image_data = request.form.get('image_data')
    weight = request.form.get('weight')

    if image_data is not None:
        print("Got image data")

        # fixes transmission hiccup that happens
        data_url = replace_spaces_with_plus(image_data)

        # Extract the base64 string
        image_data = data_url.split(',', 1)[-1]

        # Check if the string is valid base64
        if is_valid_base64(image_data):
            print("Base64 is valid")
            # If valid base64, proceed with decoding
            binary_data = base64.b64decode(image_data)

            # Save the binary data as an image file
            with open('received_image.jpg', 'wb') as f:
                f.write(binary_data)

            file_size = os.path.getsize('received_image.jpg')
            if file_size > 0:
                print(f"File created, size: {file_size} bytes")
            else:
                print("File size is 0, image data might not have been written correctly")

            test_model('received_image.jpg')

            return {'status': 'success'}
        else:
            print("Invalid base64 data")
            return {'status': 'error', 'message': 'Invalid base64 string'}
    else:
        print("image_data is none")
        return {'status': 'error', 'message': 'Invalid image_data send'}

def home():
    abort(405)

def is_valid_base64(string):
    logger = logging.getLogger(__name__)

    if len(string) % 4 != 0:  # base64 length should be a multiple of 4
        logger.error("Invalid base64 string: Length is not a multiple of 4.")
        return False

    if re.match('^[A-Za-z0-9+/=]+\Z', string) is None:  # check for invalid characters
        logger.error("Invalid base64 string: Contains invalid characters or does not match base64 pattern.")
        return False

    return True