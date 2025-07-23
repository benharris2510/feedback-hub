import pytest
from app.models import User


def test_register_user(client):
    """Test user registration"""
    response = client.post("/api/auth/register", json={
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password123"
    })
    
    assert response.status_code == 201
    assert "access_token" in response.json
    assert "refresh_token" in response.json
    assert response.json["user"]["email"] == "newuser@example.com"


def test_register_duplicate_email(client):
    """Test registration with duplicate email"""
    # First registration
    client.post("/api/auth/register", json={
        "email": "user@example.com",
        "username": "user1",
        "password": "password123"
    })
    
    # Try to register with same email
    response = client.post("/api/auth/register", json={
        "email": "user@example.com",
        "username": "user2",
        "password": "password123"
    })
    
    assert response.status_code == 400
    assert "Email already registered" in response.json["message"]


def test_login_success(client):
    """Test successful login"""
    # Create user
    user = User(email="login@example.com", username="loginuser")
    user.set_password("password123")
    from app import db
    db.session.add(user)
    db.session.commit()
    
    # Login
    response = client.post("/api/auth/login", json={
        "email": "login@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post("/api/auth/login", json={
        "email": "invalid@example.com",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
    assert "Invalid email or password" in response.json["message"]


def test_get_profile(client, auth_headers):
    """Test getting user profile"""
    response = client.get("/api/auth/profile", headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json["email"] == "test@example.com"
    assert response.json["username"] == "testuser"


def test_get_profile_unauthorized(client):
    """Test getting profile without authentication"""
    response = client.get("/api/auth/profile")
    
    assert response.status_code == 401