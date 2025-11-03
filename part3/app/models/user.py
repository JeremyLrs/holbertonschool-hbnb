import re
import uuid
from app import db, bcrypt
from datetime import datetime
from app.models.base_model import BaseModel

regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class User(BaseModel):
    """Class representing a user (Task 5 — no SQLAlchemy mapping yet)."""

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    places = db.relationship('Place', back_populates='owner', passive_deletes=True, lazy=True)
    reviews = db.relationship('Review', back_populates='user', passive_deletes=True, lazy=True)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        from app import bcrypt 
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from app import bcrypt 
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
