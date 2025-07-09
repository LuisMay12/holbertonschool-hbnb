from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    
    # Initial configurations
    app.config.from_object(config_class)
    
    # Initialize API v1
    from app.api import init_app as init_api_v1
    init_api_v1(app)
    
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    return app
