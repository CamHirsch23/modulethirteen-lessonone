import pytest
from app import create_app, db
from app.models import Customer

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_customer(client):
    response = client.post('/customers/', json={
        'name': 'Jane Doe',
        'email': 'jane@example.com',
        'phone': '1234567890'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Customer created successfully'

def test_get_customers(client):
    client.post('/customers/', json={'name': 'Jane Doe', 'email': 'jane@example.com', 'phone': '1234567890'})
    response = client.get('/customers/')
    assert response.status_code == 200
    assert len(response.get_json()) == 1