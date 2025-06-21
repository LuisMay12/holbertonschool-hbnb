import unittest
import uuid
from app import create_app

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()


class TestReviewEndpoints(BaseTestCase):
    def setUp(self):
        super().setUp()
        # User
        res = self.client.post('/api/v1/users/', json={
            "first_name": "Eva", "last_name": "Green", "email": f"{uuid.uuid4()}@example.com"
        })
        self.user_id = res.get_json()['id']
        # Amenity
        res = self.client.post('/api/v1/amenities/', json={"name": f"{uuid.uuid4()}"})
        self.assertEqual(res.status_code, 201, msg=res.get_json())
        amenity_id = res.get_json()['id']
        # Place
        res = self.client.post('/api/v1/places/', json={
            "title": "Loft",
            "price": 80,
            "latitude": 45,
            "longitude": 10,
            "owner_id": self.user_id,
            "amenities": [amenity_id]
        })
        self.place_id = res.get_json()['id']

    def test_create_review_valid(self):
        res = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(res.status_code, 201)

    def test_create_review_invalid_rating(self):
        res = self.client.post('/api/v1/reviews/', json={
            "text": "Bad range",
            "rating": 9,  # invalid
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(res.status_code, 400)

    def test_get_reviews_for_place(self):
        self.client.post('/api/v1/reviews/', json={
            "text": "Nice again",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        res = self.client.get(f'/api/v1/reviews/places/{self.place_id}/reviews')
        self.assertEqual(res.status_code, 200)

    def test_delete_review(self):
        res = self.client.post('/api/v1/reviews/', json={
            "text": "To delete",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = res.get_json()['id']
        res = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(res.status_code, 200)
