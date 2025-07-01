from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    # Configuraciones iniciales
    app.config.from_object('config.config')
    
    # Inicializar API v1
    from app.api import init_app as init_api_v1
    init_api_v1(app)


   

    return app

    
