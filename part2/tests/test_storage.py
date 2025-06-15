import pytest
from hbnb.models.engine.storage import Storage
from hbnb.models.user import User

def test_storage_singleton():
    storage1 = Storage()
    storage2 = Storage()
    assert storage1 is storage2

def test_new_and_all():
    storage = Storage()
    user = User(email="test@example.com", password="test")
    storage.new(user)
    assert len(storage.all(User)) == 1
