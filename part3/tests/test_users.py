import unittest
from app import create_app

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_valid_user(self):
        res = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com"
        })
        self.assertEqual(res.status_code, 201)

    def test_create_invalid_email(self):
        res = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "invalid"
        })
        self.assertEqual(res.status_code, 400)
