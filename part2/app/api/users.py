from flask_restx import Namespace, Resource, fields
from flask import request
from business.facade import HBnBFacade

facade = HBnBFacade()

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.String(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True)
})

user_input_model = api.model('UserInput', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        return facade.get_all_users()

    @api.expect(user_input_model)
    @api.marshal_with(user_model, code=201)
    @api.response(400, 'Invalid input')
    def post(self):
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            api.abort(400, 'Email and password are required')
        if facade.get_user_by_email(data['email']):
            api.abort(400, 'User already exists')
        user = facade.create_user(
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data['email'],
            password=data['password']
        )
        return user, 201

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class User(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user

    @api.expect(user_input_model)
    @api.marshal_with(user_model)
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input')
    def put(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        data = request.get_json()
        if not data:
            api.abort(400, 'No data provided')
        updated_user = facade.update_user(
            user_id=user_id,
            first_name=data.get('first_name', user.first_name),
            last_name=data.get('last_name', user.last_name),
            email=data.get('email', user.email),
            password=data.get('password')
        )
        return updated_user
