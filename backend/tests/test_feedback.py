import pytest
from app import db
from app.models import Feedback, User


def test_list_public_feedback(client):
    """Test listing public feedback"""
    # Create test feedback
    user = User(email="feedbacker@example.com", username="feedbacker")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()
    
    feedback1 = Feedback(
        title="Public Feedback",
        description="This is public",
        is_public=True,
        user_id=user.id,
        type="feature",
        votes=10
    )
    feedback2 = Feedback(
        title="Private Feedback",
        description="This is private",
        is_public=False,
        user_id=user.id
    )
    db.session.add_all([feedback1, feedback2])
    db.session.commit()
    
    response = client.get("/api/feedback")
    
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Public Feedback"


def test_create_feedback_authenticated(client, auth_headers):
    """Test creating feedback with authentication"""
    feedback_data = {
        "title": "New Feature Request",
        "description": "Please add this feature",
        "type": "feature",
        "priority": "high"
    }
    
    response = client.post("/api/feedback", json=feedback_data, headers=auth_headers)
    
    assert response.status_code == 201
    assert response.json["title"] == "New Feature Request"
    assert response.json["type"] == "feature"
    assert response.json["priority"] == "high"


def test_create_feedback_anonymous(client):
    """Test creating feedback without authentication"""
    feedback_data = {
        "title": "Anonymous Feedback",
        "description": "This is anonymous feedback",
        "type": "general"
    }
    
    response = client.post("/api/feedback", json=feedback_data)
    
    assert response.status_code == 201
    assert response.json["title"] == "Anonymous Feedback"
    assert response.json["user"] == "Anonymous"


def test_filter_feedback_by_status(client):
    """Test filtering feedback by status"""
    user = User(email="user@example.com", username="user")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()
    
    # Create feedback with different statuses
    feedback1 = Feedback(
        title="Open Feedback",
        description="This is open",
        status="open",
        is_public=True,
        user_id=user.id
    )
    feedback2 = Feedback(
        title="Resolved Feedback",
        description="This is resolved",
        status="resolved",
        is_public=True,
        user_id=user.id
    )
    db.session.add_all([feedback1, feedback2])
    db.session.commit()
    
    # Filter by status
    response = client.get("/api/feedback?status=open")
    
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["status"] == "open"


def test_vote_feedback(client):
    """Test voting on feedback"""
    user = User(email="user@example.com", username="user")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()
    
    feedback = Feedback(
        title="Vote Test",
        description="Test voting",
        is_public=True,
        user_id=user.id,
        votes=5
    )
    db.session.add(feedback)
    db.session.commit()
    
    response = client.post(f"/api/feedback/{feedback.id}/vote")
    
    assert response.status_code == 200
    assert response.json["votes"] == 6


def test_update_feedback_admin_only(client, admin_headers, auth_headers):
    """Test that only admins can update feedback status"""
    user = User(email="user@example.com", username="user")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()
    
    feedback = Feedback(
        title="Status Test",
        description="Test status update",
        status="open",
        is_public=True,
        user_id=user.id
    )
    db.session.add(feedback)
    db.session.commit()
    
    update_data = {
        "status": "in_progress",
        "priority": "urgent"
    }
    
    # Try with regular user
    response = client.put(f"/api/feedback/{feedback.id}", json=update_data, headers=auth_headers)
    assert response.status_code == 403
    
    # Try with admin
    response = client.put(f"/api/feedback/{feedback.id}", json=update_data, headers=admin_headers)
    assert response.status_code == 200
    assert response.json["status"] == "in_progress"
    assert response.json["priority"] == "urgent"