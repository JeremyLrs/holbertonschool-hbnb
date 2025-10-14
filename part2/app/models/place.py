from .base_model import BaseModel
from datetime import datetime


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        self.price = int(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)

        if not title or len(title) > 100:
            raise ValueError(
                "The title is required"
                "and must be less than 100 characters.")
        if self.price <= 0:
            raise ValueError("price must be positive")
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("The latitude must be between -90 and 90.")

        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("The longitude must be between -180 and 180.")

        self.title = title
        self.description = description
        self.owner = owner
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

        # Add this place to the owner's list
        owner.add_place(self)

    def add_review(self, review):
        """Add a review to the place."""
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
