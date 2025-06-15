from flask import Blueprint
from flask_restx import Api
from api.v1.views.users import api as users_ns
from api.v1.views.amenities import api as amenities_ns

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

api = Api(app_views,
          title='HBnB API',
          version='1.0',
          description='API for HBnB clone')

api.add_namespace(users_ns)
api.add_namespace(amenities_ns)
