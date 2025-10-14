import re
from .base_model import BaseModel
from datetime import datetime


class User(BaseModel):
    """ class represent an user"""
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        if not first_name or len(first_name) > 50:
            raise ValueError(
                "first_name is required"
                "and must be less than 50 characters.")
        if not last_name or len(last_name) > 50:
            raise ValueError("last_name is required"
                             "and must be less than 50 characters.")
        if not self.is_valid_email(email):
            raise ValueError("invalid email.")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.places = []
        self.reviews = []

    def is_valid_email(self, email):
        """ check if the email format is valid"""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def add_place(self, place):
        """Adds a location to the user's places list."""
        if place not in self.places:
            self.places.append(place)

    def add_review(self, review):
        """Adds a review to the user's list of reviews."""
        if review not in self.reviews:
            self.reviews.append(review)
