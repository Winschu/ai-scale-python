import logging
import os

from flask import Flask
from werkzeug.exceptions import RequestEntityTooLarge

from src.image_processing import upload_image, handle_file_size_too_large, home

os.environ['SERVER_PORT'] = '8083'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = Flask(__name__)

app.config["ENV"] = 'development'
app.config["TESTING"] = True
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024

app.register_error_handler(RequestEntityTooLarge, handle_file_size_too_large)
app.add_url_rule("/upload_image", view_func=upload_image, methods=['POST'])
app.add_url_rule("/", view_func=home, methods=['POST'])

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    print("Ready")
    print("Using Port: {0}".format(str(os.getenv('SERVER_PORT'))))
    app.run(debug=True, host='0.0.0.0', port=os.getenv('SERVER_PORT'))
