import logging

from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageFile
from dataclasses import dataclass
import io

from utils import apply_phashes, download_file

# https://github.com/python-pillow/Pillow/issues/1510
ImageFile.LOAD_TRUNCATED_IMAGES = True

app = Flask(__name__)
CORS(app)


@dataclass
class PerceptualHashes:
    blockhash: str
    neuralhash: str
    colourhash: str


@app.route("/process_image", methods=["POST"])
def process_image():
    if "file" not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify(error="No selected file"), 400
    if file:
        try:
            image_data = file.read()
            image = Image.open(io.BytesIO(image_data))
            hashes = apply_phashes(image)
            # Validate output with dataclass
            perceptual_hashes_for_image = PerceptualHashes(**hashes)
            return jsonify(perceptual_hashes_for_image.__dict__)
        except Exception as e:
            return jsonify(error=str(e)), 400

# When using the chrome extension, it will send the image as a URL
# NOTE: only do this temporarily for the demo, making the server download arbitrary files is categorically unsafe
@app.route("/process_image_url", methods=["POST"])
def process_image_url():
    if not request.form:
        return jsonify(error="No url provided"), 400
    if "url" not in request.form:
        return jsonify(error="No url provided"), 400

    url = request.form.get("url")
    
    # Download the linked image
    image_data = download_file(url)
    if not image_data :
        return jsonify(error="Failed to fetch provided image"), 400

    if image_data :
        try:
            image = Image.open(io.BytesIO(image_data))
            hashes = apply_phashes(image)
            # Validate output with dataclass
            perceptual_hashes_for_image = PerceptualHashes(**hashes)
            return jsonify(perceptual_hashes_for_image.__dict__)
        except Exception as e:
            return jsonify(error=str(e)), 400


if __name__ == "__main__":
    app.run(port=8080, debug=True)
