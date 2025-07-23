from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from app.services.auth_service import AuthService

auth_ns = Namespace("auth", description="Authentication operations")

# Models for API documentation
user_registration = auth_ns.model("UserRegistration", {
    "email": fields.String(required=True, description="User email"),
    "username": fields.String(required=True, description="Username"),
    "password": fields.String(required=True, description="Password")
})

user_login = auth_ns.model("UserLogin", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="Password")
})

token_response = auth_ns.model("TokenResponse", {
    "access_token": fields.String(description="JWT access token"),
    "refresh_token": fields.String(description="JWT refresh token"),
    "user": fields.Raw(description="User information")
})

user_response = auth_ns.model("UserResponse", {
    "id": fields.Integer(description="User ID"),
    "email": fields.String(description="User email"),
    "username": fields.String(description="Username"),
    "is_admin": fields.Boolean(description="Admin status"),
    "created_at": fields.DateTime(description="Account creation date")
})


@auth_ns.route("/register")
class UserRegister(Resource):
    @auth_ns.expect(user_registration)
    @auth_ns.response(201, "User created successfully")
    @auth_ns.response(400, "Validation error")
    def post(self):
        data = request.get_json()
        
        # Validate input
        if not data.get("email") or not data.get("username") or not data.get("password"):
            return {"message": "Email, username and password are required"}, 400
        
        # Register user
        user, error = AuthService.register_user(
            email=data["email"],
            username=data["username"],
            password=data["password"]
        )
        
        if error:
            return {"message": error}, 400
        
        # Auto-login after registration
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict()
        }, 201


@auth_ns.route("/login")
class UserLogin(Resource):
    @auth_ns.expect(user_login)
    @auth_ns.marshal_with(token_response)
    @auth_ns.response(200, "Login successful")
    @auth_ns.response(401, "Invalid credentials")
    def post(self):
        data = request.get_json()
        
        if not data.get("email") or not data.get("password"):
            return {"message": "Email and password are required"}, 400
        
        access_token, refresh_token, error = AuthService.login_user(
            email=data["email"],
            password=data["password"]
        )
        
        if error:
            return {"message": error}, 401
        
        # Get user by email since we don't have JWT identity yet during login
        from app.models.user import User
        user = User.query.filter_by(email=data["email"]).first()
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict() if user else None
        }, 200


@auth_ns.route("/refresh")
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    @auth_ns.response(200, "Token refreshed")
    @auth_ns.response(401, "Invalid refresh token")
    def post(self):
        current_user_id = get_jwt_identity()
        access_token = create_access_token(identity=current_user_id)
        
        return {
            "access_token": access_token
        }, 200


@auth_ns.route("/profile")
class UserProfile(Resource):
    @jwt_required()
    @auth_ns.marshal_with(user_response)
    @auth_ns.response(200, "Success")
    @auth_ns.response(401, "Unauthorized")
    def get(self):
        current_user_id = get_jwt_identity()
        user = AuthService.get_user_by_id(current_user_id)
        
        if not user:
            return {"message": "User not found"}, 404
        
        return user.to_dict(), 200