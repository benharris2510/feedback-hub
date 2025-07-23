import pytest
from app import create_app, db
from app.models import User, Forum

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app("testing")
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Create authenticated headers"""
    # Create test user
    user = User(email="test@example.com", username="testuser")
    user.set_password("testpass")
    db.session.add(user)
    db.session.commit()
    
    # Login and get token
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "testpass"
    })
    
    token = response.json["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client):
    """Create admin authenticated headers"""
    # Create admin user
    admin = User(email="admin@example.com", username="admin", is_admin=True)
    admin.set_password("adminpass")
    db.session.add(admin)
    db.session.commit()
    
    # Login and get token
    response = client.post("/api/auth/login", json={
        "email": "admin@example.com",
        "password": "adminpass"
    })
    
    token = response.json["access_token"]
    return {"Authorization": f"Bearer {token}"}