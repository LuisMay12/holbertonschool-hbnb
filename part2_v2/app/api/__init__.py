from flask import Blueprint
from flask_restx import Api
from .users import api as users_ns

# Configuración del Blueprint y API
blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(blueprint,
          title='HBnB API',
          version='1.0',
          description='Holiday Homes Booking API',
          doc='/doc/')  # Opcional: habilita la documentación Swagger UI

# Registrar namespaces
api.add_namespace(users_ns)

def init_app(app):
    """Función de inicialización para registrar el blueprint en la app Flask"""
    app.register_blueprint(blueprint)
