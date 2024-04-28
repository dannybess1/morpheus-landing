from models.image_record import ImageRecord
from phashes import PERCEPTUAL_HASHES
from typing import Optional
from database import db

class PhashService:
    """
    PhashService
    A convenience wrapper of static methods to interact with the database
    """

    # TODO: types on this?
    @staticmethod
    def add_phash(url: str, phashes: dict) -> bool:
        # TODO: create conversion method / lineup names
        new_phashes = ImageRecord(url=url, block_hash=phashes["blockhash"], neural_hash=phashes["neuralhash"], color_hash=phashes["colourhash"])
        try:
            db.session.add(new_phashes)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            # TODO: manage
            print(f"Failed to add phashes to db: {e}")
            return False

    @staticmethod
    def get_from_id(id: int) -> Optional[ImageRecord]:
        """
        Given an id, return the ImageRecord
        """
        return ImageRecord.query.get(id)

    @staticmethod
    def get_from_url(url: str) -> Optional[ImageRecord]:
        """
        Given a url, return the ImageRecord
        """
        return ImageRecord.query.filter_by(url=url).first()

