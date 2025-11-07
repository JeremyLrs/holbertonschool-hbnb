import re
import uuid
from datetime import datetime
from app import db, bcrypt
from app.models.base_model import BaseModel

class User(BaseModel, db.Model):
    """User model with SQLAlchemy mapping and validation."""

    __tablename__ = 'users'

    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    places = db.relationship('Place', back_populates='owner', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='author', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        """Initialize the user, ensuring valid email and hashed password."""
        super().__init__(*args, **kwargs)

        for key, value in kwargs.items():
            if hasattr(self,key):
                setattr(self,key,value)
                
        if 'email' in kwargs and not self.is_valid_email(kwargs['email']):
            raise ValueError("Invalid email format.")
        if 'password' in kwargs and kwargs['password']:
            self.hash_password(kwargs['password'])

    def hash_password(self, password):
        """Hashes the password before storing it."""
        if password:
            self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def is_valid_email(self, email):
        """Validates email format using regex."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def add_place(self, place):
        """Adds a place to the user's list of places."""
        if place not in self.places:
            self.places.append(place)

    def add_review(self, review):
        """Adds a review to the user's list of reviews."""
        if review not in self.reviews:
            self.reviews.append(review)

    def update(self, data):
        """Safely update user attributes."""
        for key, value in data.items():
            if key in ['first_name', 'last_name', 'email']:
                if key == 'email' and not self.is_valid_email(value):
                    raise ValueError("Invalid email format.")
                if key in ['first_name', 'last_name']:
                    if not value or len(value) > 50:
                        raise ValueError(f"{key} is required and must be less than 50 characters.")
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def to_dict(self):
        """Serialize user instance to dictionary (excluding password)."""
        user_dict = super().to_dict()
        if 'password' in user_dict:
            del user_dict['password']
        return user_dict

    def __repr__(self):
        return f"<User {self.email} (Admin={self.is_admin})>"
