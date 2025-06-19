from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnb Application Api', doc='/api/v1/')

    # Placeholder for Api namespaces (serán agregados más tarde)
    # Adiditional namespaces for places, reviews, and amenities will be added later

    return app