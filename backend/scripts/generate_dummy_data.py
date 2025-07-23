import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Forum, ForumPost, PostReply, Feedback, FeedbackComment
from datetime import datetime, timedelta
import random

app = create_app()

def generate_dummy_data():
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create users
        print("Creating users...")
        users = []
        
        # Admin user
        admin = User(email="admin@feedbackhub.com", username="admin", is_admin=True)
        admin.set_password("admin123")
        users.append(admin)
        db.session.add(admin)
        
        # Regular users
        for i in range(1, 6):
            user = User(
                email=f"user{i}@example.com",
                username=f"user{i}",
                is_admin=False
            )
            user.set_password("password123")
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        
        # Create forums
        print("Creating forums...")
        forum_data = [
            {
                "name": "General Discussion",
                "description": "Talk about anything related to our platform",
                "is_public": True
            },
            {
                "name": "Feature Requests",
                "description": "Suggest new features and improvements",
                "is_public": True
            },
            {
                "name": "Bug Reports",
                "description": "Report bugs and technical issues",
                "is_public": True
            },
            {
                "name": "Developer Corner",
                "description": "API discussions and developer resources",
                "is_public": True
            }
        ]
        
        forums = []
        for data in forum_data:
            forum = Forum(
                name=data["name"],
                description=data["description"],
                is_public=data["is_public"],
                user_id=admin.id
            )
            forums.append(forum)
            db.session.add(forum)
        
        db.session.commit()
        
        # Create posts
        print("Creating forum posts...")
        post_titles = [
            "Welcome to Feedback Hub!",
            "How to use the API effectively",
            "Best practices for collecting user feedback",
            "New features coming soon",
            "Platform maintenance schedule",
            "Integration with third-party tools",
            "Mobile app development update",
            "Community guidelines and rules",
            "Success stories from our users",
            "Troubleshooting common issues"
        ]
        
        posts = []
        for i, title in enumerate(post_titles):
            forum = random.choice(forums)
            author = random.choice(users)
            
            post = ForumPost(
                forum_id=forum.id,
                user_id=author.id,
                title=title,
                content=f"This is the content for {title}. Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                       f"Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
                       f"Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
                views=random.randint(10, 500),
                is_pinned=(i == 0),  # Pin the first post
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            posts.append(post)
            db.session.add(post)
        
        db.session.commit()
        
        # Create replies
        print("Creating post replies...")
        reply_contents = [
            "Great post! Thanks for sharing.",
            "I have a question about this.",
            "This helped me solve my problem.",
            "Can you provide more details?",
            "I agree with your points.",
            "Has anyone else experienced this?",
            "Looking forward to the updates!",
            "This is exactly what I was looking for."
        ]
        
        for post in posts[:7]:  # Add replies to first 7 posts
            num_replies = random.randint(1, 5)
            for _ in range(num_replies):
                reply = PostReply(
                    post_id=post.id,
                    user_id=random.choice(users).id,
                    content=random.choice(reply_contents),
                    created_at=post.created_at + timedelta(hours=random.randint(1, 48))
                )
                db.session.add(reply)
        
        db.session.commit()
        
        # Create feedback
        print("Creating feedback...")
        feedback_data = [
            {
                "title": "Add dark mode support",
                "description": "It would be great to have a dark mode option for better visibility at night.",
                "type": "feature",
                "priority": "high",
                "status": "open",
                "votes": 45
            },
            {
                "title": "Export data to CSV format",
                "description": "Allow users to export their feedback data in CSV format for analysis.",
                "type": "feature",
                "priority": "medium",
                "status": "in_progress",
                "votes": 32
            },
            {
                "title": "Login page not loading properly",
                "description": "Sometimes the login page takes too long to load or shows a blank screen.",
                "type": "bug",
                "priority": "urgent",
                "status": "resolved",
                "votes": 12
            },
            {
                "title": "Improve search functionality",
                "description": "The search feature could be more accurate and faster.",
                "type": "improvement",
                "priority": "medium",
                "status": "open",
                "votes": 28
            },
            {
                "title": "Add webhook support",
                "description": "Integration with webhooks would help automate workflows.",
                "type": "feature",
                "priority": "low",
                "status": "open",
                "votes": 15
            },
            {
                "title": "Mobile app crashes on startup",
                "description": "The iOS app crashes immediately after opening on iPhone 12.",
                "type": "bug",
                "priority": "urgent",
                "status": "in_progress",
                "votes": 8
            },
            {
                "title": "Add real-time notifications",
                "description": "Push notifications for new feedback and responses would be helpful.",
                "type": "feature",
                "priority": "medium",
                "status": "open",
                "votes": 38
            },
            {
                "title": "Improve documentation",
                "description": "More examples and tutorials in the documentation would help new users.",
                "type": "general",
                "priority": "low",
                "status": "closed",
                "votes": 22
            }
        ]
        
        feedbacks = []
        for data in feedback_data:
            feedback = Feedback(
                user_id=random.choice(users).id if random.random() > 0.2 else None,  # 20% anonymous
                title=data["title"],
                description=data["description"],
                type=data["type"],
                priority=data["priority"],
                status=data["status"],
                votes=data["votes"],
                is_public=True,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 60))
            )
            feedbacks.append(feedback)
            db.session.add(feedback)
        
        db.session.commit()
        
        # Create feedback comments
        print("Creating feedback comments...")
        comment_contents = [
            "This is a great idea!",
            "We're working on this feature.",
            "Thanks for reporting this issue.",
            "This has been fixed in the latest version.",
            "Can you provide more details about this?",
            "This is planned for the next release.",
            "We appreciate your feedback!",
            "This is now available in beta."
        ]
        
        for feedback in feedbacks[:6]:  # Add comments to first 6 feedbacks
            num_comments = random.randint(1, 4)
            for i in range(num_comments):
                commenter = random.choice(users)
                comment = FeedbackComment(
                    feedback_id=feedback.id,
                    user_id=commenter.id,
                    content=random.choice(comment_contents),
                    is_admin_response=(commenter.is_admin or i == 0),  # First comment or admin comments
                    created_at=feedback.created_at + timedelta(hours=random.randint(1, 72))
                )
                db.session.add(comment)
        
        db.session.commit()
        
        print("\nDummy data generated successfully!")
        print(f"Created {len(users)} users (1 admin, {len(users)-1} regular)")
        print(f"Created {len(forums)} forums")
        print(f"Created {len(posts)} forum posts")
        print(f"Created {len(feedbacks)} feedback items")
        print("\nAdmin credentials:")
        print("Email: admin@feedbackhub.com")
        print("Password: admin123")
        print("\nRegular user credentials:")
        print("Email: user1@example.com (through user5@example.com)")
        print("Password: password123")


if __name__ == "__main__":
    generate_dummy_data()