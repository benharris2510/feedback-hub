from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restx import Api

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name="development"):
    app = Flask(__name__)
    
    # Load config
    if config_name == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    elif config_name == "testing":
        app.config.from_object("app.config.TestingConfig")
    elif config_name == "production":
        app.config.from_object("app.config.ProductionConfig")
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize API
    api = Api(
        app,
        title="Feedback Hub API",
        version="1.0",
        description="A comprehensive user feedback and forum platform API",
        prefix="/api",
        doc="/api/docs"
    )
    
    # Register namespaces
    from app.api.auth import auth_ns
    from app.api.forums import forums_ns
    from app.api.feedback import feedback_ns
    from app.api.posts import posts_ns
    
    api.add_namespace(auth_ns)
    api.add_namespace(forums_ns)
    api.add_namespace(feedback_ns)
    api.add_namespace(posts_ns)
    
    return app