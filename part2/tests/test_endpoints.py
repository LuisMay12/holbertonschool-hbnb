import pytest
from hbnb.app import app
from models.engine.storage import storage

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_user(client):
    response = client.post('/api/v1/users/', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert b'test@example.com' in response.data

def test_get_users(client):
    response = client.get('/api/v1/users/')
    assert response.status_code == 200
    assert isinstance(response.json, list)

# Similar tests for other endpoints...
