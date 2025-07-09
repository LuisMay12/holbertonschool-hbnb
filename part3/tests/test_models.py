import unittest
from app.models.user import User
from app.models.place import Place

class TestModels(unittest.TestCase):
    def test_user_validation(self):
        with self.assertRaises(ValueError):
            User(first_name="A"*51, last_name="Doe", email="test@example.com")
            
    def test_place_coordinates(self):
        with self.assertRaises(ValueError):
            Place(title="Test", latitude=100, longitude=0, owner_id="user123")

if __name__ == '__main__':
    unittest.main()
