from .base_model import BaseModel
from datetime import datetime


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        if not name or len(name) > 50:
            raise ValueError(
                "The amenity name is required"
                "and must be less than 50 characters.")

        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
