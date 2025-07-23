import pytest
from app import db
from app.models import Forum, User


def test_list_public_forums(client):
    """Test listing public forums"""
    # Create test forums
    user = User(email="creator@example.com", username="creator")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()
    
    forum1 = Forum(name="Public Forum", description="A public forum", is_public=True, user_id=user.id)
    forum2 = Forum(name="Private Forum", description="A private forum", is_public=False, user_id=user.id)
    db.session.add_all([forum1, forum2])
    db.session.commit()
    
    response = client.get("/api/forums")
    
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Public Forum"


def test_create_forum_admin_only(client, admin_headers, auth_headers):
    """Test that only admins can create forums"""
    forum_data = {
        "name": "New Forum",
        "description": "A new forum",
        "is_public": True
    }
    
    # Try with regular user
    response = client.post("/api/forums", json=forum_data, headers=auth_headers)
    assert response.status_code == 403
    
    # Try with admin
    response = client.post("/api/forums", json=forum_data, headers=admin_headers)
    assert response.status_code == 201
    assert response.json["name"] == "New Forum"
    assert response.json["slug"] == "new-forum"


def test_get_forum_by_slug(client):
    """Test getting forum by slug"""
    user = User(email="creator@example.com", username="creator")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()
    
    forum = Forum(name="Test Forum", description="Test", is_public=True, user_id=user.id)
    db.session.add(forum)
    db.session.commit()
    
    response = client.get(f"/api/forums/slug/{forum.slug}")
    
    assert response.status_code == 200
    assert response.json["name"] == "Test Forum"


def test_update_forum_admin_only(client, admin_headers):
    """Test updating forum"""
    user = User(email="creator@example.com", username="creator")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()
    
    forum = Forum(name="Original Name", description="Original", is_public=True, user_id=user.id)
    db.session.add(forum)
    db.session.commit()
    
    update_data = {
        "name": "Updated Name",
        "description": "Updated description"
    }
    
    response = client.put(f"/api/forums/{forum.id}", json=update_data, headers=admin_headers)
    
    assert response.status_code == 200
    assert response.json["name"] == "Updated Name"
    assert response.json["description"] == "Updated description"


def test_delete_forum_admin_only(client, admin_headers):
    """Test deleting forum"""
    user = User(email="creator@example.com", username="creator")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()
    
    forum = Forum(name="To Delete", description="Will be deleted", is_public=True, user_id=user.id)
    db.session.add(forum)
    db.session.commit()
    
    response = client.delete(f"/api/forums/{forum.id}", headers=admin_headers)
    
    assert response.status_code == 204
    assert Forum.query.get(forum.id) is None