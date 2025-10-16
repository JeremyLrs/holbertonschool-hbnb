from .base_model import BaseModel
from datetime import datetime


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text:
            raise ValueError("The review text is required.")
        if not (1 <= rating <= 5):
            raise ValueError("The rating must be between 1 and 5.")
        if not place or not user:
            raise ValueError(
                "The review must be associated"
                "with a location and a user.")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        place.add_review(self)
        user.add_review(self)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user.id,
            'place_id': self.place.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
