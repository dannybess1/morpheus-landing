import logging

from flask import request, jsonify, Blueprint
from PIL import Image, ImageFile
from dataclasses import dataclass
import io

from utils import apply_phashes, download_file
from services.cloud_storage import CloudStorageService
from services.pinecone import PineconeService
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

            logging.info(f"Phashes for image {url}: {hashes}")

            # We do not have a url for this image, so we want to upload it to google cloud storage
            # Then return the db
            # TODO: should the filename be a uuid?
            url = CloudStorageService().upload_file(file.filename, image_data)
            
            # Add hashes to vector db
            PineconeService().insert(url, hashes)

            # Add hashes to the database
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
    
    logging.info(f"Successfully Downloaded image from {url}")

    if image_data:
        try:
            image = Image.open(io.BytesIO(image_data))
            hashes = apply_phashes(image)


            # Validate output with dataclass
            perceptual_hashes_for_image = PerceptualHashes(**hashes)
            url = CloudStorageService().upload_file(url, image_data)

            logging.info(f"Phashes for image {url}: {hashes}")

            # We store the twitter url here rather than 
            # Add hashes to vector db
            PineconeService().insert(url, hashes)

            # Add hashes to the database
            PhashService.add_phash(url, perceptual_hashes_for_image)


            return jsonify(perceptual_hashes_for_image.__dict__)
        except Exception as e:
            return jsonify(error=str(e)), 400
    else:
        return jsonify(error="Failed to fetch provided image"), 500

# Helper method to view database entries
@main.route("/get_phashes", methods=["GET"])
def get_db_page():
    """
    Read database page from query param
    """
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=25, type=int)

    try:
        images = PhashService.get_page(page, limit)
        return jsonify(images), 200
    except Exception as e:
        return jsonify(error=str(e)), 400
