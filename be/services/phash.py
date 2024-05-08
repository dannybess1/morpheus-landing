from models.image_record import ImageRecord
from phashes import PERCEPTUAL_HASHES
from typing import Optional
from database import db
import logging

class PhashService:
    """
    PhashService
    A convenience wrapper of static methods to interact with the database
    """

    # TODO: types on this?
    @staticmethod
    def add_phash(url: str, phashes: dict) -> bool:
        # TODO: create conversion method / lineup names
        new_phashes = ImageRecord(url=url, block_hash=phashes.blockhash, neural_hash=phashes.neuralhash, color_hash=phashes.colourhash)
        try:
            db.session.add(new_phashes)
            db.session.commit()
            logging.info(f"Added phashes to db for {url}")
            return True
        except Exception as e:
            db.session.rollback()
            # TODO: manage
            logging.error(f"Failed to add phashes to db: {e}")
            return False

    @staticmethod
    def get_from_id(id: int) -> Optional[ImageRecord]:
        """
        Given an id, return the ImageRecord
        """
        return ImageRecord.query.get(id)
    
    @staticmethod
    def get_page(page: int, limit: int = 25) -> list[ImageRecord]:
        """
        Given a page and limit, return limit the ImageRecords
        """
        images = ImageRecord.query.paginate(page=page, per_page=limit)

        return_images = []
        for image in images.items:
            return_images.append({
                "id": image.id,
                "url": image.url,
                "block_hash": image.block_hash,
                "neural_hash": image.neural_hash,
                "color_hash": image.color_hash
            })
        return return_images

    @staticmethod
    def get_from_url(url: str) -> Optional[ImageRecord]:
        """
        Given a url, return the ImageRecord
        """
        return ImageRecord.query.filter_by(url=url).first()

