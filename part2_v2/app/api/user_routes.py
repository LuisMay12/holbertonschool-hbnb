from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from app.business.user_facade import UserFacade

user_bp = Blueprint("users", __name__, url_prefix="/api/v1")
api = Api(user_bp, doc="/api/v1/docs", title="HBnB User API")
ns = api.namespace("users", description="User operations")

facade = UserFacade()

user_model = api.model("User", {
    "id": fields.String(readonly=True),
    "email": fields.String(request=True),
    "password" : fields.String(request=True),
    "first_name": fields.String,
    "last_name": fields.String
})

user_response = api.model("UserResponse", {
    "id": fields.String,
    "email": fields.String,
    "first_name": fields.String,
    "last_name": fields.String
})

@ns.route("/")
class userList(Resource):
    @ns.marshal_list_with(user_response)
    def get(self):
        users = facade.get_all_users()
        return [u.to_dict() for u in users]

    @ns.expect(user_model)
    @ns.marshal_with(user_response, code=201)
    def post(self):
        data = request.json()
        user = facade.create_user(data)
        return user.to_dict(), 201

@ns.route("/<string:user_id>")
@ns.response(404, "User not found")
class UserResource(Resource):
    @ns.marshal_with(user_response)
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict()

    @ns.expect(user_model)
    @ns.marshal_with(user_response)
    def put(self, user_id):
        data = request.json
        user = facade.update_user(user_id, data)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict()