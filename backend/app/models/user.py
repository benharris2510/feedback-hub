from datetime import datetime
from app import db
import bcrypt


class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    forums = db.relationship("Forum", backref="creator", lazy="dynamic")
    posts = db.relationship("ForumPost", backref="author", lazy="dynamic")
    replies = db.relationship("PostReply", backref="author", lazy="dynamic")
    feedbacks = db.relationship("Feedback", backref="user", lazy="dynamic")
    feedback_comments = db.relationship("FeedbackComment", backref="user", lazy="dynamic")
    api_keys = db.relationship("ApiKey", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<User {self.username}>"