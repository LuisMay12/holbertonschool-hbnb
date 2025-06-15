from datetime import datetime
from hbnb.models.base_model import BaseMode

def test_base_model_init():
    model = BaseModel()
    assert isinstance(model.id, str)
    assert isinstance(model.created_at, datetime)
    assert isinstance(model.updated_at, datetime)

def test_base_model_save():
    model = BaseModel()
    old_updated = model.updated_at
    model.save()
    assert model.updated_at > old_updated
