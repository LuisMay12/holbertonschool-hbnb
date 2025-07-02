from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_indentity, get_jwt
from app.services.facade import hbnb_facade

api = Namespace('Places', description='Place operations', path='/places')
api = Namespace('admin', description='Admin operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email')
})

# Define the place model for input validation and documentation
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title'),
    'description': fields.String(description='Description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='Owner ID'),
    'amenities': fields.List(fields.String, required=True, description="List of Amenity IDs")
})

place_output_model = api.inherit('PlaceOutput', place_input_model, {
    'id': fields.String(description='Place ID'),
    'owner': fields.Nested(user_model),
    'amenities': fields.List(fields.Nested(amenity_model))
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_input_model, validate=True)
    @api.response(201, 'Place created successfully')
    @api.marshal_with(place_output_model, code = 201)
    @jwt_required()
    def psot(self):
        """Create a new place"""
        current_user = get_jwt_idnetity()
        # Logic to create a new place for the logged-in user
        pass
    @api.response(400, 'Invalid input')
    def post(self):
        """Register a new place"""
        data = api.payload
        try:
            place = hbnb_facade.create_place(data)
            return place, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.marshal_list_with(place_output_model, code = 200)
    def get(self):
        """Retrieve all places"""
        return hbnb_facade.get_all_places()

# /api/v1/places/<place_id>
@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_output_model, code = 200)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve a place by ID with owner and amenities"""
        place = hbnb_facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return place

    @api.expect(place_input_model, validate=True)
    @api.marshal_with(place_output_model, code = 200)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input')
    def put(self, place_id):
        """Update a place's information"""
        data = api.payload
        try:
            hbnb_facade.update_place(place_id, data)
            return hbnb_facade.get_place(place_id)
        except ValueError as e:
            api.abort(400, str(e))

    
    @api.route('/<place_id>')
    class PlaceResource(Resource):
        @jwt_required()
        def put(self, place_id):
            current_user = get_jwt_identity()
            place = facade.get._place(place_id)
            if place.owner_id != current_user:
                return {'error': 'Unauthorized action'}, 403
            # Logic to update the place
            pass

    