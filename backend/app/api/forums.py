from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Forum, User

forums_ns = Namespace("forums", description="Forum operations")

# API Models
forum_model = forums_ns.model("Forum", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True, description="Forum name"),
    "description": fields.String(description="Forum description"),
    "slug": fields.String(readonly=True),
    "is_public": fields.Boolean(default=True),
    "posts_count": fields.Integer(readonly=True),
    "created_at": fields.DateTime(readonly=True),
    "creator": fields.String(readonly=True)
})

forum_create = forums_ns.model("ForumCreate", {
    "name": fields.String(required=True, description="Forum name"),
    "description": fields.String(description="Forum description"),
    "is_public": fields.Boolean(default=True)
})


@forums_ns.route("")
class ForumList(Resource):
    @forums_ns.marshal_list_with(forum_model)
    @forums_ns.doc("list_forums")
    def get(self):
        """List all public forums"""
        forums = Forum.query.filter_by(is_public=True).order_by(Forum.created_at.desc()).all()
        return [forum.to_dict() for forum in forums]
    
    @jwt_required()
    @forums_ns.expect(forum_create)
    @forums_ns.marshal_with(forum_model)
    @forums_ns.doc("create_forum")
    @forums_ns.response(201, "Forum created")
    @forums_ns.response(400, "Validation error")
    def post(self):
        """Create a new forum"""
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Check if user is admin
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return {"message": "Admin access required"}, 403
        
        forum = Forum(
            name=data.get("name"),
            description=data.get("description"),
            is_public=data.get("is_public", True),
            user_id=current_user_id
        )
        
        db.session.add(forum)
        db.session.commit()
        
        return forum.to_dict(), 201


@forums_ns.route("/<int:id>")
@forums_ns.param("id", "The forum identifier")
class ForumDetail(Resource):
    @forums_ns.marshal_with(forum_model)
    @forums_ns.doc("get_forum")
    @forums_ns.response(404, "Forum not found")
    def get(self, id):
        """Get a specific forum"""
        forum = Forum.query.get_or_404(id)
        
        # Check if forum is public
        if not forum.is_public:
            return {"message": "Forum is private"}, 403
        
        return forum.to_dict()
    
    @jwt_required()
    @forums_ns.expect(forum_create)
    @forums_ns.marshal_with(forum_model)
    @forums_ns.doc("update_forum")
    @forums_ns.response(200, "Forum updated")
    @forums_ns.response(403, "Access denied")
    @forums_ns.response(404, "Forum not found")
    def put(self, id):
        """Update a forum"""
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        forum = Forum.query.get_or_404(id)
        
        # Check if user is admin
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return {"message": "Admin access required"}, 403
        
        forum.name = data.get("name", forum.name)
        forum.description = data.get("description", forum.description)
        forum.is_public = data.get("is_public", forum.is_public)
        
        db.session.commit()
        
        return forum.to_dict()
    
    @jwt_required()
    @forums_ns.doc("delete_forum")
    @forums_ns.response(204, "Forum deleted")
    @forums_ns.response(403, "Access denied")
    @forums_ns.response(404, "Forum not found")
    def delete(self, id):
        """Delete a forum"""
        current_user_id = get_jwt_identity()
        
        forum = Forum.query.get_or_404(id)
        
        # Check if user is admin
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return {"message": "Admin access required"}, 403
        
        db.session.delete(forum)
        db.session.commit()
        
        return "", 204


@forums_ns.route("/slug/<string:slug>")
@forums_ns.param("slug", "The forum slug")
class ForumBySlug(Resource):
    @forums_ns.marshal_with(forum_model)
    @forums_ns.doc("get_forum_by_slug")
    @forums_ns.response(404, "Forum not found")
    def get(self, slug):
        """Get a forum by slug"""
        forum = Forum.query.filter_by(slug=slug).first_or_404()
        
        # Check if forum is public
        if not forum.is_public:
            return {"message": "Forum is private"}, 403
        
        return forum.to_dict()