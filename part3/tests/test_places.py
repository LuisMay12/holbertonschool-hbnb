import unittest
import uuid
from app import create_app

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    

class TestPlaceEndpoints(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create user
        res = self.client.post('/api/v1/users/', json={
            "first_name": "Bob", "last_name": "Marley", "email":f"{uuid.uuid4()}@example.com"
        })
        self.assertEqual(res.status_code, 201, msg=res.get_json())
        self.owner_id = res.get_json()['id']
        # Create amenity
        res = self.client.post('/api/v1/amenities/', json={"name": f"{uuid.uuid4()}Pool"})
        self.assertEqual(res.status_code, 201, msg=res.get_json())
        self.amenity_id = res.get_json()['id']

    def test_create_place_valid(self):
        res = self.client.post('/api/v1/places/', json={
            "title": "Seaside House",
            "description": "Beautiful view",
            "price": 120,
            "latitude": 25.0,
            "longitude": -80.0,
            "owner_id": self.owner_id,
            "amenities": [self.amenity_id]
        })
        self.assertEqual(res.status_code, 201)

    def test_create_place_invalid_coords(self):
        res = self.client.post('/api/v1/places/', json={
            "title": "Nowhere",
            "price": 100,
            "latitude": 95.0,  # Invalid
            "longitude": -200.0,  # Invalid
            "owner_id": self.owner_id,
            "amenities": [self.amenity_id]
        })
        self.assertEqual(res.status_code, 400)

    def test_get_all_places(self):
        res = self.client.get('/api/v1/places/')
        self.assertEqual(res.status_code, 200)
