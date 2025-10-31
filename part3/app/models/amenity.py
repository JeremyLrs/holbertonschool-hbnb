import uuid
from app import db
from datetime import datetime


class Amenity(db.Model):
    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name):
        super().__init__()

        if not name or len(name) > 50:
            raise ValueError(
                "The amenity name is required"
                "and must be less than 50 characters.")

        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
