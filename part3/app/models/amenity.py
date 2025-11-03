import uuid
from datetime import datetime
from app import db


class Amenity(db.Model):
    """SQLAlchemy model representing an Amenity (Task 8 & 9)."""

    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    places = db.relationship(
        "Place",
        secondary="place_amenity",
        back_populates="amenities",
        lazy="subquery"
    )

    def __init__(self, name, description=None):
        """Initialize an Amenity with validation."""
        super().__init__()

        if not name or len(name.strip()) == 0 or len(name) > 128:
            raise ValueError("Amenity name is required and must be less than 128 characters.")

        self.name = name.strip()
        self.description = description
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self, include_related=False):
        """Serialize amenity object to dictionary."""
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_related:
            data["places"] = [{"id": p.id, "title": p.title} for p in self.places]

        return data

    def __repr__(self):
        return f"<Amenity {self.name}>"
