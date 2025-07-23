from datetime import datetime
from app import db


class Feedback(db.Model):
    __tablename__ = "feedbacks"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # Allow anonymous feedback
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="open")  # open, in_progress, resolved, closed
    type = db.Column(db.String(50), default="general")  # bug, feature, general, improvement
    priority = db.Column(db.String(20), default="medium")  # low, medium, high, urgent
    votes = db.Column(db.Integer, default=0)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    comments = db.relationship("FeedbackComment", backref="feedback", lazy="dynamic", cascade="all, delete-orphan")
    
    def upvote(self):
        self.votes += 1
        db.session.commit()
    
    def downvote(self):
        if self.votes > 0:
            self.votes -= 1
            db.session.commit()
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "type": self.type,
            "priority": self.priority,
            "votes": self.votes,
            "is_public": self.is_public,
            "comments_count": self.comments.count(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user": self.user.username if self.user else "Anonymous"
        }
    
    def __repr__(self):
        return f"<Feedback {self.title}>"


class FeedbackComment(db.Model):
    __tablename__ = "feedback_comments"
    
    id = db.Column(db.Integer, primary_key=True)
    feedback_id = db.Column(db.Integer, db.ForeignKey("feedbacks.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_admin_response = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "feedback_id": self.feedback_id,
            "user_id": self.user_id,
            "content": self.content,
            "is_admin_response": self.is_admin_response,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user": self.user.username if self.user else None
        }
    
    def __repr__(self):
        return f"<FeedbackComment {self.id}>"