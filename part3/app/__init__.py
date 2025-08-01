from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    
    CORS(app)
    
    # Initial configurations
    app.config.from_object(config_class)
    
    # Initialize API v1
    from app.api import init_app as init_api_v1
    init_api_v1(app)
    
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    # Initialize the database when running the app
    with app.app_context():
        db.create_all()  # Create database tables based on models
    
    return app
