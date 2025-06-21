import unittest
from app import create_app

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()


class TestAmenityEndpoints(BaseTestCase):
    def test_create_amenity(self):
        res = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        self.assertEqual(res.status_code, 201)

    def test_create_duplicate_amenity(self):
        self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        res = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        self.assertEqual(res.status_code, 400)

    def test_get_amenity_list(self):
        res = self.client.get('/api/v1/amenities/')
        self.assertEqual(res.status_code, 200)
