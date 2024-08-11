import pytest
from app import create_app, db
from app.models import Production, Product

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

def test_create_production(client):
    client.post('/products/', json={'name': 'Widget', 'price': 19.99})
    response = client.post('/production/', json={
        'product_id': 1,
        'quantity_produced': 100,
        'date_produced': '2024-08-11'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Production record created successfully'

def test_get_production(client):
    client.post('/products/', json={'name': 'Widget', 'price': 19.99})
    client.post('/production/', json={'product_id': 1, 'quantity_produced': 100, 'date_produced': '2024-08-11'})
    response = client.get('/production/')
    assert response.status_code == 200
    assert len(response.get_json()) == 1