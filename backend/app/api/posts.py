from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import ForumPost, PostReply, Forum, User

posts_ns = Namespace("posts", description="Forum posts operations")

# API Models
post_model = posts_ns.model("Post", {
    "id": fields.Integer(readonly=True),
    "forum_id": fields.Integer(required=True),
    "title": fields.String(required=True),
    "content": fields.String(required=True),
    "views": fields.Integer(readonly=True),
    "is_pinned": fields.Boolean(readonly=True),
    "is_locked": fields.Boolean(readonly=True),
    "replies_count": fields.Integer(readonly=True),
    "created_at": fields.DateTime(readonly=True),
    "updated_at": fields.DateTime(readonly=True),
    "author": fields.String(readonly=True),
    "forum": fields.String(readonly=True)
})

post_create = posts_ns.model("PostCreate", {
    "title": fields.String(required=True, description="Post title"),
    "content": fields.String(required=True, description="Post content")
})

reply_model = posts_ns.model("Reply", {
    "id": fields.Integer(readonly=True),
    "post_id": fields.Integer(readonly=True),
    "content": fields.String(required=True),
    "created_at": fields.DateTime(readonly=True),
    "author": fields.String(readonly=True)
})

reply_create = posts_ns.model("ReplyCreate", {
    "content": fields.String(required=True, description="Reply content")
})


@posts_ns.route("/forum/<int:forum_id>")
@posts_ns.param("forum_id", "The forum identifier")
class ForumPosts(Resource):
    @posts_ns.marshal_list_with(post_model)
    @posts_ns.doc("list_forum_posts")
    def get(self, forum_id):
        """List all posts in a forum"""
        forum = Forum.query.get_or_404(forum_id)
        
        if not forum.is_public:
            return {"message": "Forum is private"}, 403
        
        posts = ForumPost.query.filter_by(forum_id=forum_id)\
            .order_by(ForumPost.is_pinned.desc(), ForumPost.created_at.desc()).all()
        
        return [post.to_dict() for post in posts]
    
    @jwt_required()
    @posts_ns.expect(post_create)
    @posts_ns.marshal_with(post_model)
    @posts_ns.doc("create_post")
    @posts_ns.response(201, "Post created")
    @posts_ns.response(400, "Validation error")
    def post(self, forum_id):
        """Create a new post in a forum"""
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Check if forum exists and is public
        forum = Forum.query.get_or_404(forum_id)
        if not forum.is_public:
            return {"message": "Cannot post to private forum"}, 403
        
        post = ForumPost(
            forum_id=forum_id,
            user_id=current_user_id,
            title=data.get("title"),
            content=data.get("content")
        )
        
        db.session.add(post)
        db.session.commit()
        
        return post.to_dict(), 201


@posts_ns.route("/<int:id>")
@posts_ns.param("id", "The post identifier")
class PostDetail(Resource):
    @posts_ns.marshal_with(post_model)
    @posts_ns.doc("get_post")
    @posts_ns.response(404, "Post not found")
    def get(self, id):
        """Get a specific post"""
        post = ForumPost.query.get_or_404(id)
        
        # Check if forum is public
        if not post.forum.is_public:
            return {"message": "Post is in a private forum"}, 403
        
        # Increment views
        post.increment_views()
        
        return post.to_dict()
    
    @jwt_required()
    @posts_ns.expect(post_create)
    @posts_ns.marshal_with(post_model)
    @posts_ns.doc("update_post")
    @posts_ns.response(200, "Post updated")
    @posts_ns.response(403, "Access denied")
    def put(self, id):
        """Update a post"""
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        post = ForumPost.query.get_or_404(id)
        
        # Check if user is author or admin
        user = User.query.get(current_user_id)
        if post.user_id != current_user_id and not user.is_admin:
            return {"message": "Access denied"}, 403
        
        if post.is_locked and not user.is_admin:
            return {"message": "Post is locked"}, 403
        
        post.title = data.get("title", post.title)
        post.content = data.get("content", post.content)
        
        db.session.commit()
        
        return post.to_dict()
    
    @jwt_required()
    @posts_ns.doc("delete_post")
    @posts_ns.response(204, "Post deleted")
    @posts_ns.response(403, "Access denied")
    def delete(self, id):
        """Delete a post"""
        current_user_id = get_jwt_identity()
        
        post = ForumPost.query.get_or_404(id)
        
        # Check if user is author or admin
        user = User.query.get(current_user_id)
        if post.user_id != current_user_id and not user.is_admin:
            return {"message": "Access denied"}, 403
        
        db.session.delete(post)
        db.session.commit()
        
        return "", 204


@posts_ns.route("/<int:id>/replies")
@posts_ns.param("id", "The post identifier")
class PostReplies(Resource):
    @posts_ns.marshal_list_with(reply_model)
    @posts_ns.doc("list_post_replies")
    def get(self, id):
        """List all replies to a post"""
        post = ForumPost.query.get_or_404(id)
        
        # Check if forum is public
        if not post.forum.is_public:
            return {"message": "Post is in a private forum"}, 403
        
        replies = PostReply.query.filter_by(post_id=id)\
            .order_by(PostReply.created_at.asc()).all()
        
        return [reply.to_dict() for reply in replies]
    
    @jwt_required()
    @posts_ns.expect(reply_create)
    @posts_ns.marshal_with(reply_model)
    @posts_ns.doc("create_reply")
    @posts_ns.response(201, "Reply created")
    @posts_ns.response(400, "Validation error")
    def post(self, id):
        """Create a reply to a post"""
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        post = ForumPost.query.get_or_404(id)
        
        # Check if post is locked
        if post.is_locked:
            return {"message": "Post is locked"}, 403
        
        # Check if forum is public
        if not post.forum.is_public:
            return {"message": "Cannot reply to post in private forum"}, 403
        
        reply = PostReply(
            post_id=id,
            user_id=current_user_id,
            content=data.get("content")
        )
        
        db.session.add(reply)
        db.session.commit()
        
        return reply.to_dict(), 201


@posts_ns.route("/<int:id>/lock")
@posts_ns.param("id", "The post identifier")
class PostLock(Resource):
    @jwt_required()
    @posts_ns.doc("lock_post")
    @posts_ns.response(200, "Post locked/unlocked")
    @posts_ns.response(403, "Admin access required")
    def put(self, id):
        """Lock or unlock a post"""
        current_user_id = get_jwt_identity()
        
        # Check if user is admin
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return {"message": "Admin access required"}, 403
        
        post = ForumPost.query.get_or_404(id)
        post.is_locked = not post.is_locked
        
        db.session.commit()
        
        return {"is_locked": post.is_locked}, 200


@posts_ns.route("/<int:id>/pin")
@posts_ns.param("id", "The post identifier")
class PostPin(Resource):
    @jwt_required()
    @posts_ns.doc("pin_post")
    @posts_ns.response(200, "Post pinned/unpinned")
    @posts_ns.response(403, "Admin access required")
    def put(self, id):
        """Pin or unpin a post"""
        current_user_id = get_jwt_identity()
        
        # Check if user is admin
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return {"message": "Admin access required"}, 403
        
        post = ForumPost.query.get_or_404(id)
        post.is_pinned = not post.is_pinned
        
        db.session.commit()
        
        return {"is_pinned": post.is_pinned}, 200