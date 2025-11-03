import uuid
from datetime import datetime
from app import db


class Review(db.Model):
    """SQLAlchemy model representing a Review (Task 8 & 9)."""

    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.String(512), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author = db.relationship('User', back_populates='reviews')
    place = db.relationship('Place', back_populates='reviews')

    def __init__(self, text, rating, user, place):
        """Initialize a Review with validation."""
        super().__init__()

        if not text:
            raise ValueError("The review text is required.")
        if not (1 <= int(rating) <= 5):
            raise ValueError("The rating must be between 1 and 5.")
        if not user or not place:
            raise ValueError("A review must be linked to both a user and a place.")

        self.text = text
        self.rating = int(rating)
        self.author = user
        self.place = place
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        if place and hasattr(place, "add_review"):
            place.add_review(self)
        if user and hasattr(user, "add_review"):
            user.add_review(self)

    def to_dict(self, include_related=False):
        """Convert review object to dictionary."""
        data = {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_related:
            data["author"] = {
                "id": self.author.id,
                "first_name": self.author.first_name,
                "last_name": self.author.last_name,
                "email": self.author.email
            }
            data["place"] = {
                "id": self.place.id,
                "title": getattr(self.place, "title", None)
            }

        return data

    def __repr__(self):
        return f"<Review {self.id} by {self.user_id} for Place {self.place_id}>"
