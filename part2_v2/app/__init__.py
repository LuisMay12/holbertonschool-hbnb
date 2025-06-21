from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    
    # Configuraciones iniciales
    app.config.from_object('config.config')
    
    # Inicializar API v1
    from app.api import init_app as init_api_v1
    init_api_v1(app)
    
    return app
