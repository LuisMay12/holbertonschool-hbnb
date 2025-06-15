from flask_restx import Namespace, Resource, fields
from flask import request
from hbnb.api.v1.services.user_service import UserService

api = Namespace('users', description='User operations')

# Modelo para documentación API
user_model = api.model('User', {
    'id': fields.String(readonly=True, description='User identifier'),
    'email': fields.String(required=True, description='Email address'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

user_input_model = api.model('UserInput', {
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        users, _, _ = UserService.get_all_users()
        return users

    @api.expect(user_input_model)
    @api.marshal_with(user_model, code=201)
    @api.response(400, 'Invalid input')
    def post(self):
        """Create a new user"""
        user, error_msg, status_code = UserService.create_user(request.get_json())
        if error_msg:
            api.abort(status_code, error_msg)
        return user, status_code

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get a specific user"""
        user, error_msg, status_code = UserService.get_user(user_id)
        if error_msg:
            api.abort(status_code, error_msg)
        return user

    @api.expect(user_input_model)
    @api.marshal_with(user_model)
    @api.response(400, 'Invalid input')
    def put(self, user_id):
        """Update a user"""
        user, error_msg, status_code = UserService.update_user(user_id, request.get_json())
        if error_msg:
            api.abort(status_code, error_msg)
        return user
