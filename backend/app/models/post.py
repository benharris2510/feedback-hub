from datetime import datetime
from app import db


class ForumPost(db.Model):
    __tablename__ = "forum_posts"
    
    id = db.Column(db.Integer, primary_key=True)
    forum_id = db.Column(db.Integer, db.ForeignKey("forums.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    views = db.Column(db.Integer, default=0)
    is_pinned = db.Column(db.Boolean, default=False)
    is_locked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    replies = db.relationship("PostReply", backref="post", lazy="dynamic", cascade="all, delete-orphan")
    
    def increment_views(self):
        self.views += 1
        db.session.commit()
    
    def to_dict(self):
        return {
            "id": self.id,
            "forum_id": self.forum_id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content,
            "views": self.views,
            "is_pinned": self.is_pinned,
            "is_locked": self.is_locked,
            "replies_count": self.replies.count(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "author": self.author.username if self.author else None,
            "forum": self.forum.name if self.forum else None
        }
    
    def __repr__(self):
        return f"<ForumPost {self.title}>"


class PostReply(db.Model):
    __tablename__ = "post_replies"
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("forum_posts.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "author": self.author.username if self.author else None
        }
    
    def __repr__(self):
        return f"<PostReply {self.id}>"