import re
import uuid
from datetime import datetime
from app import db, bcrypt
from app.models.base_model import BaseModel


class User(db.Model, BaseModel):
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

    def __init__(self, **kwargs):

        if 'first_name' not in kwargs and 'email' not in kwargs:
            raise ValueError("User must be created with valid data")

        super().__init__(**kwargs)

        if 'email' in kwargs and not self.is_valid_email(kwargs['email']):
            raise ValueError("Invalid email format.")

        if 'password' in kwargs:
            self.hash_password(kwargs['password'])

    def hash_password(self, password):
        """Hash password before storing."""
        if password:
            self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Check password."""
        return bcrypt.check_password_hash(self.password, password)

    def is_valid_email(self, email):
        """Very basic email format validation."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def add_place(self, place):
        if place not in self.places:
            self.places.append(place)

    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)

    def update(self, data):
        """Update allowed user fields."""
        for key, value in data.items():
            if key in ['first_name', 'last_name', 'email']:
                if key == 'email' and not self.is_valid_email(value):
                    raise ValueError("Invalid email format.")
                setattr(self, key, value)

        self.updated_at = datetime.utcnow()
        db.session.commit()

    def __repr__(self):
        return f"<User {self.email} (Admin={self.is_admin})>"
