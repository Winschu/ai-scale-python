from flask import Flask, request, jsonify
import base64

app = Flask(__name__)


@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Empfange das Bild als Base64-codierten String von Arduino
    image_data = request.form.get('image_data')

    # Dekodiere den Base64-String zu Binärdaten
    binary_data = base64.b64decode(image_data)

    # Speichere die Binärdaten als Bilddatei
    with open('received_image.jpg', 'wb') as f:
        f.write(binary_data)

    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)
