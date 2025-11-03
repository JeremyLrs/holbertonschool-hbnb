import uuid
from app import db
from datetime import datetime


class Place(db.Model):
    __tablename__ = "places"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512))
    price = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, title, description, price, latitude,
                 longitude, owner_id, amenities=None):
        super().__init__()

        # main fields
        self.title = title
        self.description = description
        self.price = int(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)

        self.owner_id = owner_id

        # Dates
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # Relations
        self.reviews = []
        self.amenities = amenities or []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or len(value) > 100:
            raise ValueError(
                "The title is required"
                "and must be less than 100 characters.")
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        value = float(value)
        if value < 0:
            raise ValueError("price must be positive")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        value = float(value)
        if not (-90.0 <= value <= 90.0):
            raise ValueError("The latitude must be between -90 and 90.")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        value = float(value)
        if not (-180.0 <= value <= 180.0):
            raise ValueError("The longitude must be between -180 and 180.")
        self._longitude = value

    def add_review(self, review):
        """Add a review to the place."""
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self, include_related=False):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": (
                [a.id for a in self.amenities]
                if self.amenities
                else []
            ),
            "reviews": [r.id for r in self.reviews] if include_related else []
        }

    @classmethod
    def get(cls, place_id):
        for p in cls._places:
            if p.id == place_id:
                return p
        return None

    @classmethod
    def get_all(cls):
        return cls._places
