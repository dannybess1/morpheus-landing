from database import db

# TODO: not entirely sure an sql db is the most suitable if we are looking up based on distance
class ImageRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # TODO: will the image url need to be true - we also may not always get one so it can be nullable
    url = db.Column(db.String(255), unique=True, nullable=True)
    block_hash = db.Column(db.String(64), unique=False, nullable=True)
    neural_hash = db.Column(db.String(64), unique=False, nullable=True)
    color_hash = db.Column(db.String(64), unique=False, nullable=True)

    def __repr__(self):
        return f"<ImageRecord {self.url}, {self.image_hash}>"