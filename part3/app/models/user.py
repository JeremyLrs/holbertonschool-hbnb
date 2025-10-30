import re
import uuid
from app import db, bcrypt
from datetime import datetime
from app.models.base_model import BaseModel

regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class User(BaseModel):
    """Class representing a user (Task 5 — no SQLAlchemy mapping yet)."""

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("first_name is required and must be less than 50 characters.")
        if not last_name or len(last_name) > 50:
            raise ValueError("last_name is required and must be less than 50 characters.")
        if not self.is_valid_email(email):
            raise ValueError("Invalid email format.")

        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

        if password:
            self.hash_password(password)
        else:
            self.password = None

    def hash_password(self, password):
        """Hashes the password before storing it."""
        from app import bcrypt  # ✅ import local to avoid circular import
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from app import bcrypt  # ✅ import local to avoid circular import
        return bcrypt.check_password_hash(self.password, password)

    def is_valid_email(self, email):
        """Check if the email format is valid"""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def add_place(self, place):
        """Adds a place to the user's places list"""
        if place not in self.places:
            self.places.append(place)

    def add_review(self, review):
        """Adds a review to the user's reviews list"""
        if review not in self.reviews:
            self.reviews.append(review)

    def update(self, data):
        """Update user attributes"""
        for key, value in data.items():
            if key in ['first_name', 'last_name', 'email']:
                if key == 'email' and not self.is_valid_email(value):
                    raise ValueError("Invalid email format.")
                if key in ['first_name', 'last_name']:
                    if not value or len(value) > 50:
                        raise ValueError(f"{key} is required and must be less than 50 characters.")
                setattr(self, key, value)
        self.updated_at = datetime.now()
