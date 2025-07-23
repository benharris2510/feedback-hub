from datetime import datetime
import secrets
from app import db


class ApiKey(db.Model):
    __tablename__ = "api_keys"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    key = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    last_used_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(ApiKey, self).__init__(**kwargs)
        if not self.key:
            self.key = self.generate_key()
    
    @staticmethod
    def generate_key():
        return f"fh_{secrets.token_urlsafe(32)}"
    
    def update_last_used(self):
        self.last_used_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "key": self.key[:8] + "..." + self.key[-4:],  # Partial key for security
            "is_active": self.is_active,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<ApiKey {self.name}>"