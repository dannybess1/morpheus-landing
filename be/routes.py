import logging

from flask import request, jsonify, Blueprint
from PIL import Image, ImageFile
from dataclasses import dataclass
import io

from utils import apply_phashes, download_file
from services.cloud_storage import CloudStorageService
from services.phash import PhashService

# https://github.com/python-pillow/Pillow/issues/1510
ImageFile.LOAD_TRUNCATED_IMAGES = True

main = Blueprint('main', __name__)

@dataclass
class PerceptualHashes:
    blockhash: str
    neuralhash: str
    colourhash: str



@main.route("/process_image", methods=["POST"])
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

            # We do not have a url for this image, so we want to upload it to google cloud storage
            # Then return the db
            # TODO: should the filename be a uuid?
            url = CloudStorageService().upload_file(file.filename, image_data)
            PhashService.add_phash(url, perceptual_hashes_for_image)
            

            return jsonify(perceptual_hashes_for_image.__dict__)
        except Exception as e:
            return jsonify(error=str(e)), 400

from constants import TWITTER_IMG_PREFIX

# When using the chrome extension, it will send the image as a URL
# NOTE: only do this temporarily for the demo, making the server download arbitrary files is categorically unsafe
# To temporarily work around this we limit images to come from the twitter domain
@main.route("/process_image_url", methods=["POST"])
def process_image_url():
    if not request.form:
        return jsonify(error="No url provided"), 400
    if "url" not in request.form:
        return jsonify(error="No url provided"), 400

    url = request.form.get("url")
    if not url.startswith(TWITTER_IMG_PREFIX):
        return jsonify(error="Invalid image URL"), 400
    
    # Download the linked image
    image_data = download_file(url)
    if not image_data :
        return jsonify(error="Failed to fetch provided image"), 500

    if image_data:
        try:
            image = Image.open(io.BytesIO(image_data))
            hashes = apply_phashes(image)

            # Validate output with dataclass
            perceptual_hashes_for_image = PerceptualHashes(**hashes)

            # We store the twitter url here rather than 
            PhashService.add_phash(url, perceptual_hashes_for_image)

            return jsonify(perceptual_hashes_for_image.__dict__)
        except Exception as e:
            return jsonify(error=str(e)), 400
    else:
        return jsonify(error="Failed to fetch provided image"), 500
