from flask import Blueprint
from flask_restx import Api
from .v1.users import api as users_ns
from .v1.amenities import api as amenities_ns
from .v1.places import api as places_ns

# Configuración del Blueprint y API
blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(blueprint,
          title='HBnB API',
          version='1.0',
          description='Holiday Homes Booking API',
          doc='/doc/')

# namespaces
api.add_namespace(users_ns)
api.add_namespace(amenities_ns)
api.add_namespace(places_ns)

def init_app(app):
    """Función de inicialización para registrar el blueprint en la app Flask"""
    app.register_blueprint(blueprint)
