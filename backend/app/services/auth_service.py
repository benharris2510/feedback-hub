from flask_jwt_extended import create_access_token, create_refresh_token
from app import db
from app.models.user import User


class AuthService:
    @staticmethod
    def register_user(email, username, password):
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return None, "Email already registered"
        
        if User.query.filter_by(username=username).first():
            return None, "Username already taken"
        
        # Create new user
        user = User(email=email, username=username)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user, None
    
    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return None, None, "Invalid email or password"
        
        if not user.is_active:
            return None, None, "Account is deactivated"
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return access_token, refresh_token, None
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)