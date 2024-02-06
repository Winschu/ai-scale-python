from testModel import test_model

from flask import Flask, request
import base64
import os
import re

import logging

from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 128 * 1024 * 1024

@app.errorhandler(RequestEntityTooLarge)
def handle_file_size_too_large(e):
    difference = request.content_length - app.config['MAX_CONTENT_LENGTH']
    return f"Die Datei ist zu groß. Sie überschreitet das Limit um {difference} Bytes.", 413


def replace_spaces_with_plus(base64_string: str):
    return base64_string.replace(' ', '+')


@app.route("/upload_image", methods=['POST'])
def upload_image():
    # Receive the base64 encoded image
    image_data = request.form.get('image_data')
    weight = request.form.get("weight")

    if image_data is not None:
        # fixes transmission hiccup that happens
        data_url = replace_spaces_with_plus(image_data)

        # Extract the base64 string
        image_data = data_url.split(',', 1)[-1]

        print(data_url)

        # Check if the string is valid base64
        if is_valid_base64(image_data):
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
            return {'status': 'error', 'message': 'Invalid base64 string'}
    else:
        print("data_url is none: ")
        print(image_data)


def is_valid_base64(string):
    logger = logging.getLogger(__name__)

    if len(string) % 4 != 0:  # base64 length should be a multiple of 4
        logger.error("Invalid base64 string: Length is not a multiple of 4.")
        return False

    if re.match('^[A-Za-z0-9+/=]+\Z', string) is None:  # check for invalid characters
        logger.error("Invalid base64 string: Contains invalid characters or does not match base64 pattern.")
        return False

    return True

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
