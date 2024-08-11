import pytest
from app import create_app, db
from app.models import Employee

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

def test_create_employee(client):
    response = client.post('/employees/', json={
        'name': 'John Doe',
        'position': 'Manager'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Employee created successfully'

def test_get_employees(client):
    client.post('/employees/', json={'name': 'John Doe', 'position': 'Manager'})
    response = client.get('/employees/')
    assert response.status_code == 200
    assert len(response.get_json()) == 1