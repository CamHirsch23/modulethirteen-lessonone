import pytest
from app import create_app, db
from app.models import Order, Customer, Product

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

def test_create_order(client):
    client.post('/customers/', json={'name': 'Jane Doe', 'email': 'jane@example.com', 'phone': '1234567890'})
    client.post('/products/', json={'name': 'Widget', 'price': 19.99})
    response = client.post('/orders/', json={
        'customer_id': 1,
        'product_id': 1,
        'quantity': 2,
        'total_price': 39.98
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Order created successfully'

def test_get_orders(client):
    client.post('/customers/', json={'name': 'Jane Doe', 'email': 'jane@example.com', 'phone': '1234567890'})
    client.post('/products/', json={'name': 'Widget', 'price': 19.99})
    client.post('/orders/', json={'customer_id': 1, 'product_id': 1, 'quantity': 2, 'total_price': 39.98})
    response = client.get('/orders/')
    assert response.status_code == 200
    assert len(response.get_json()) == 1