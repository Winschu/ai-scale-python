from flask import request, abort
import base64
import os
import re
import logging

from src.testModel import detect_fruit


def handle_file_size_too_large(e):
    difference = request.content_length - request.max_content_length
    return f"Die Datei ist zu groß. Sie überschreitet das Limit um {difference} Bytes.", 413


def replace_spaces_with_plus(base64_string: str):
    return base64_string.replace(' ', '+')


def upload_image():
    logger = logging.getLogger(__name__)

    # Receive the base64 encoded image
    raw_image_data = request.form.get('image_data')
    weight = request.form.get('weight')

    weight = 100

    logger.warning(f"Raw Image Data Length: {len(raw_image_data)}")

    if raw_image_data is not None:
        print("Got image data")

        # fixes transmission hiccup that happens
        data_url = replace_spaces_with_plus(raw_image_data)

        print(data_url)
        image_data = data_url.split(',', 1)[-1]

        logger.warning(f"Data Length: {len(image_data)}")

        # Check if the string is valid base64
        if is_valid_base64(image_data):
            print("Base64 is valid!")
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

            probabilities, class_index, class_label = detect_fruit('received_image.jpg')

            appel_min = 80
            appel_max = 300
            appel_range = range(appel_min, appel_max + 1)

            orange_min = 100
            orange_max = 500
            orange_range = range(orange_min, orange_max + 1)

            plum_min = 10
            plum_max = 50
            plum_range = range(plum_min, plum_max + 1)

            # Beispielbedingung für die Klassifizierung von Früchten basierend auf Gewicht und Klassenbezeichnung
            if class_label in ["Apple Braeburn", "Orange", "Plum"]:
                if (class_label == "Apple Braeburn" and weight in appel_range) or \
                        (class_label == "Orange" and weight in orange_range) or \
                        (class_label == "Plum" and weight in plum_range):
                    # Include the weight and prediction results in the response
                    return {
                        'status': 'success',
                        'weight': weight,
                        'prediction': {
                            'probabilities': probabilities,
                            'class_index': class_index,
                            'class_label': class_label
                        }
                    }
                else:
                    logger.error("Detected fruit didn't fit into the weight range")
            else:
                logger.error("Unknown fruit recognized!")

        else:
            print("Invalid base64 data")
            print(data_url)
            return {'status': 'error', 'message': 'Invalid base64 string'}

    else:
        print("image_data is none")
        return {'status': 'error', 'message': 'Invalid image_data send'}


def home():
    abort(405)


def is_valid_base64(string):
    logger = logging.getLogger(__name__)

    if len(string) % 4 != 0:  # base64 length should be a multiple of 4
        logger.error(f"Invalid base64 string: Length ({len(string)}) is not a multiple of 4.")
        return False

    if re.match('^[A-Za-z0-9+/=]+\Z', string) is None:  # check for invalid characters
        logger.error("Invalid base64 string: Contains invalid characters or does not match base64 pattern.")
        return False

    return True
