from datetime import datetime
from app import db
from slugify import slugify


class Forum(db.Model):
    __tablename__ = "forums"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    is_public = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    posts = db.relationship("ForumPost", backref="forum", lazy="dynamic", cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        super(Forum, self).__init__(**kwargs)
        if self.name and not self.slug:
            self.slug = self.generate_unique_slug()
    
    def generate_unique_slug(self):
        slug = slugify(self.name)
        counter = 1
        original_slug = slug
        
        while Forum.query.filter_by(slug=slug).first() is not None:
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        return slug
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "slug": self.slug,
            "is_public": self.is_public,
            "user_id": self.user_id,
            "posts_count": self.posts.count(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "creator": self.creator.username if self.creator else None
        }
    
    def __repr__(self):
        return f"<Forum {self.name}>"