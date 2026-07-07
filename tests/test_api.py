import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_post(client):
    response = client.post('/inventory', json={
        'id': '1',
        'name': 'Item 1',
        'quantity': 10
    })
    assert response.status_code == 201

def test_get_inventory(client):
    response = client.get('/inventory')
    assert response.status_code == 200

def test_patch(client):
    response = client.patch('/inventory/1', json={
        'name': 'Updated Item 1',
        'quantity': 20
    })
    assert response.status_code == 200
def test_delete(client):
    response = client.delete('/inventory/1')
    assert response.status_code == 200

def test_external_api(client):
    response = client.get('/product/737628064502')
    assert response.status_code in [200, 404]
