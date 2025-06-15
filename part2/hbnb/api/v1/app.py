from flask_restful import Api
from hbnb.api.v1.views.users import UserResource, UserList

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
api = Api(app_views)

api.add_resource(UserList, '/users/')
api.add_resource(UserResource, '/users/<string:user_id>')
