from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app import db
from app.models import Feedback, FeedbackComment, User, ApiKey

feedback_ns = Namespace("feedback", description="Feedback operations")

# API Models
feedback_model = feedback_ns.model("Feedback", {
    "id": fields.Integer(readonly=True),
    "title": fields.String(required=True),
    "description": fields.String(required=True),
    "status": fields.String(description="Feedback status"),
    "type": fields.String(description="Feedback type"),
    "priority": fields.String(description="Feedback priority"),
    "votes": fields.Integer(readonly=True),
    "is_public": fields.Boolean(default=True),
    "comments_count": fields.Integer(readonly=True),
    "created_at": fields.DateTime(readonly=True),
    "updated_at": fields.DateTime(readonly=True),
    "user": fields.String(readonly=True)
})

feedback_create = feedback_ns.model("FeedbackCreate", {
    "title": fields.String(required=True, description="Feedback title"),
    "description": fields.String(required=True, description="Feedback description"),
    "type": fields.String(default="general", description="Type: bug, feature, general, improvement"),
    "priority": fields.String(default="medium", description="Priority: low, medium, high, urgent"),
    "is_public": fields.Boolean(default=True)
})

feedback_update = feedback_ns.model("FeedbackUpdate", {
    "status": fields.String(description="Status: open, in_progress, resolved, closed"),
    "priority": fields.String(description="Priority: low, medium, high, urgent")
})

comment_model = feedback_ns.model("Comment", {
    "id": fields.Integer(readonly=True),
    "content": fields.String(required=True),
    "is_admin_response": fields.Boolean(readonly=True),
    "created_at": fields.DateTime(readonly=True),
    "user": fields.String(readonly=True)
})

comment_create = feedback_ns.model("CommentCreate", {
    "content": fields.String(required=True, description="Comment content")
})


def check_api_key():
    """Check for API key in headers"""
    api_key = request.headers.get("X-API-Key")
    if api_key:
        key = ApiKey.query.filter_by(key=api_key, is_active=True).first()
        if key:
            key.update_last_used()
            return key.user_id
    return None


@feedback_ns.route("")
class FeedbackList(Resource):
    @feedback_ns.marshal_list_with(feedback_model)
    @feedback_ns.doc("list_feedback")
    @feedback_ns.param("status", "Filter by status")
    @feedback_ns.param("type", "Filter by type")
    @feedback_ns.param("priority", "Filter by priority")
    def get(self):
        """List all public feedback"""
        query = Feedback.query.filter_by(is_public=True)
        
        # Apply filters
        status = request.args.get("status")
        if status:
            query = query.filter_by(status=status)
        
        type_ = request.args.get("type")
        if type_:
            query = query.filter_by(type=type_)
        
        priority = request.args.get("priority")
        if priority:
            query = query.filter_by(priority=priority)
        
        feedbacks = query.order_by(Feedback.votes.desc(), Feedback.created_at.desc()).all()
        return [feedback.to_dict() for feedback in feedbacks]
    
    @feedback_ns.expect(feedback_create)
    @feedback_ns.marshal_with(feedback_model)
    @feedback_ns.doc("create_feedback")
    @feedback_ns.response(201, "Feedback created")
    @feedback_ns.response(400, "Validation error")
    def post(self):
        """Create new feedback (requires auth or API key)"""
        data = request.get_json()
        
        # Check for authentication
        user_id = None
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            pass
        
        # If no JWT, check for API key
        if not user_id:
            user_id = check_api_key()
        
        feedback = Feedback(
            user_id=user_id,
            title=data.get("title"),
            description=data.get("description"),
            type=data.get("type", "general"),
            priority=data.get("priority", "medium"),
            is_public=data.get("is_public", True)
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        return feedback.to_dict(), 201


@feedback_ns.route("/<int:id>")
@feedback_ns.param("id", "The feedback identifier")
class FeedbackDetail(Resource):
    @feedback_ns.marshal_with(feedback_model)
    @feedback_ns.doc("get_feedback")
    @feedback_ns.response(404, "Feedback not found")
    def get(self, id):
        """Get specific feedback"""
        feedback = Feedback.query.get_or_404(id)
        
        if not feedback.is_public:
            return {"message": "Feedback is private"}, 403
        
        return feedback.to_dict()
    
    @jwt_required()
    @feedback_ns.expect(feedback_update)
    @feedback_ns.marshal_with(feedback_model)
    @feedback_ns.doc("update_feedback")
    @feedback_ns.response(200, "Feedback updated")
    @feedback_ns.response(403, "Admin access required")
    def put(self, id):
        """Update feedback status (admin only)"""
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Check if user is admin
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return {"message": "Admin access required"}, 403
        
        feedback = Feedback.query.get_or_404(id)
        
        if data.get("status"):
            feedback.status = data["status"]
        if data.get("priority"):
            feedback.priority = data["priority"]
        
        db.session.commit()
        
        return feedback.to_dict()


@feedback_ns.route("/<int:id>/vote")
@feedback_ns.param("id", "The feedback identifier")
class FeedbackVote(Resource):
    @feedback_ns.doc("vote_feedback")
    @feedback_ns.response(200, "Vote recorded")
    def post(self, id):
        """Upvote feedback"""
        feedback = Feedback.query.get_or_404(id)
        
        if not feedback.is_public:
            return {"message": "Cannot vote on private feedback"}, 403
        
        feedback.upvote()
        
        return {"votes": feedback.votes}, 200


@feedback_ns.route("/<int:id>/comments")
@feedback_ns.param("id", "The feedback identifier")
class FeedbackComments(Resource):
    @feedback_ns.marshal_list_with(comment_model)
    @feedback_ns.doc("list_comments")
    def get(self, id):
        """List comments on feedback"""
        feedback = Feedback.query.get_or_404(id)
        
        if not feedback.is_public:
            return {"message": "Feedback is private"}, 403
        
        comments = FeedbackComment.query.filter_by(feedback_id=id)\
            .order_by(FeedbackComment.created_at.asc()).all()
        
        return [comment.to_dict() for comment in comments]
    
    @jwt_required()
    @feedback_ns.expect(comment_create)
    @feedback_ns.marshal_with(comment_model)
    @feedback_ns.doc("create_comment")
    @feedback_ns.response(201, "Comment created")
    def post(self, id):
        """Add comment to feedback"""
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        feedback = Feedback.query.get_or_404(id)
        
        if not feedback.is_public:
            return {"message": "Cannot comment on private feedback"}, 403
        
        user = User.query.get(current_user_id)
        
        comment = FeedbackComment(
            feedback_id=id,
            user_id=current_user_id,
            content=data.get("content"),
            is_admin_response=user.is_admin
        )
        
        db.session.add(comment)
        db.session.commit()
        
        return comment.to_dict(), 201