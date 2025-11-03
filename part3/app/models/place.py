import uuid
from datetime import datetime
from app import db

place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id", ondelete="CASCADE"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id", ondelete="CASCADE"), primary_key=True)
)

class Place(db.Model):
    """SQLAlchemy model representing a Place (Task 8 & 9)."""

    __tablename__ = "places"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512))
    price = db.Column(db.Float, default=0.0)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner = db.relationship("User", back_populates="places", lazy=True)
    reviews = db.relationship("Review", back_populates="place", cascade="all, delete-orphan", lazy=True)
    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places",
        lazy="subquery"
    )

    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=None):
        """Initialize a Place with validation."""
        super().__init__()

        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner_id = owner_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.amenities = amenities or []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or len(value) > 100:
            raise ValueError("The title is required and must be less than 100 characters.")
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        value = float(value)
        if value < 0:
            raise ValueError("Price must be positive.")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        value = float(value)
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be between -90 and 90.")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        value = float(value)
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be between -180 and 180.")
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
        """Return a JSON-serializable dictionary."""
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_related:
            data["amenities"] = [a.to_dict() for a in self.amenities]
            data["reviews"] = [r.to_dict() for r in self.reviews]

        return data

    def __repr__(self):
        return f"<Place {self.title} (owner={self.owner_id})>"
