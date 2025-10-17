import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_place(self):
        # User Creation
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Does",
            "email": "jane.does@example.com"
        })
        user = response.get_json()

        # Place Creation: Success
        response = self.client.post('/api/v1/places/', json={
            "title": "Chalet",
            "description": "Beautiful place in front of mount.",
            "price": 225.5,
            "latitude": 55.5,
            "longitude": -15.5,
            "rooms": 5,
            "capacity": 8,
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_attributes(self):
        # User Creation
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        user = response.get_json()

        # Place Creation: Negative Price
        response = self.client.post('/api/v1/places/', json={
            "title": "Chalet",
            "description": "Beautiful place in front of mount.",
            "price": -225.5,
            "latitude": 55.5,
            "longitude": -15.5,
            "rooms": 5,
            "capacity": 8,
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

        # Place Creation: Wrong Latitude
        response = self.client.post('/api/v1/places/', json={
            "title": "Chalet",
            "description": "Beautiful place in front of mount.",
            "price": 225.5,
            "latitude": 95.0,
            "longitude": -15.5,
            "rooms": 5,
            "capacity": 8,
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

        # Place Creation: Wrong Longitude
        response = self.client.post('/api/v1/places/', json={
            "title": "Chalet",
            "description": "Beautiful place in front of mount.",
            "price": 225.5,
            "latitude": 55.5,
            "longitude": -205.0,
            "rooms": 5,
            "capacity": 8,
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_no_owner(self):
        # Place Creation: No Owner
        response = self.client.post('/api/v1/places/', json={
            "title": "Chalet",
            "description": "Beautiful place in front of mount.",
            "latitude": 95.0,
            "longitude": -15.5,
            "rooms": 5,
            "capacity": 8,
            "owner_id": "",
            "amenities": []
        })
        self.assertEqual(response.status_code, 404)

    def test_create_place_empty_attributes(self):
        # User Creation
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jonathan",
            "last_name": "Doe",
            "email": "jonathan.doe@example.com"
        })
        user = response.get_json()

        # Place Creation: No Title
        response = self.client.post('/api/v1/places/', json={
            "title": None,
            "description": "Beautiful place in front of mount.",
            "price": 225.5,
            "latitude": 95.0,
            "longitude": -15.5,
            "rooms": 5,
            "capacity": 8,
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

        # Place Creation: Empty Title
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "Beautiful place in front of mount.",
            "price": 225.5,
            "latitude": 95.0,
            "longitude": -15.5,
            "rooms": 5,
            "capacity": 8,
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

        # Place Creation: No Price
        response = self.client.post('/api/v1/places/', json={
            "title": "Chalet",
            "description": "Beautiful place in front of mount.",
            "price": None,
            "latitude": 95.0,
            "longitude": -15.5,
            "rooms": 5,
            "capacity": 8,
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

        # Place Creation: No Latitude
        response = self.client.post('/api/v1/places/', json={
            "title": "Chalet",
            "description": "Beautiful place in front of mount.",
            "price": 225.5,
            "latitude": None,
            "longitude": -15.5,
            "rooms": 5,
            "capacity": 8,
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

        # Place Creation: No Longitude
        response = self.client.post('/api/v1/places/', json={
            "title": "Chalet",
            "description": "Beautiful place in front of mount.",
            "price": 225.5,
            "latitude": 95.0,
            "longitude": None,
            "rooms": 5,
            "capacity": 8,
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
