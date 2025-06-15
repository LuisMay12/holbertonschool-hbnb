import pytest
from hbnb.models.user import User
from models.place import Place
from models.review import Review

def test_user_validation():
    # Test valid user
    valid_user = User(first_name="John", last_name="Doe", 
                     email="john@example.com", password="secure123")
    assert valid_user is not None
    
    # Test invalid email
    with pytest.raises(ValueError):
        User(email="invalid", password="pass")

def test_place_validation():
    # Test valid place
    valid_place = Place(name="Test Place", price_by_night=100)
    assert valid_place is not None
    
    # Test invalid price
    with pytest.raises(ValueError):
        Place(name="Test", price_by_night=-10)

# Similar tests for other models...
