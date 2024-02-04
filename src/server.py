from threading import Thread
import time
from flask import Flask, request
from flask_restful import Api, Resource
import base64
import os
import re
from cheroot.wsgi import Server as WSGIServer

import logging
import cherrypy

from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024

print("Current Max Length: ")
print(app.config['MAX_CONTENT_LENGTH'])

@app.errorhandler(RequestEntityTooLarge)
def handle_file_size_too_large(e):
    difference = request.content_length - app.config['MAX_CONTENT_LENGTH']
    return f"Die Datei ist zu groß. Sie überschreitet das Limit um {difference} Bytes.", 413

api = Api(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('flask.log')
app.logger.addHandler(file_handler)
cherrypy.log.error_log.setLevel(logging.INFO)


def replace_spaces_with_plus(base64_string):
    return base64_string.replace(' ', '+')


class UploadImage(Resource):
    def post(self):
        # Receive the base64 encoded image
        data_url = request.form.get('image_data')

        data_url = replace_spaces_with_plus(data_url)

        print("Data URL:")
        print(data_url)

        print(len(data_url))

        # Extract the base64 string
        image_data = data_url.split(',', 1)[-1]

        print("Image Data")
        print(image_data)

        # Check if the string is valid base64
        if self.is_valid_base64(image_data):
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

            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Invalid base64 string'}

    @staticmethod
    def is_valid_base64(string):
        logger = logging.getLogger(__name__)

        if len(string) % 4 != 0:  # base64 length should be a multiple of 4
            logger.error("Invalid base64 string: Length is not a multiple of 4.")
            return False

        if re.match('^[A-Za-z0-9+/=]+\Z', string) is None:  # check for invalid characters
            logger.error("Invalid base64 string: Contains invalid characters or does not match base64 pattern.")
            return False

        return True


api.add_resource(UploadImage, '/upload_image')  # Route_1


def start_server():
    server = WSGIServer((host, port), app)
    server.start()


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    t = Thread(target=start_server)
    t.start()
    time.sleep(1)
    if t.is_alive():
        logger.info(f'Server has successfully started and is reachable at {host}:{port}.')
    try:
        t.join()
    except KeyboardInterrupt:
        logger.info('Server has been stopped.')
