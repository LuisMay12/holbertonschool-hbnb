from flask import request
from flask_restx import Resource, Namespace, fields
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.engine.storage import storage

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'user_id': fields.String(required=True),
    'name': fields.String(required=True),
    'description': fields.String,
    'number_rooms': fields.Integer(default=0),
    'number_bathrooms': fields.Integer(default=0),
    'max_guest': fields.Integer(default=0),
    'price_by_night': fields.Integer(default=0),
    'latitude': fields.Float,
    'longitude': fields.Float,
    'amenity_ids': fields.List(fields.String)
})

@api.route('/')
class PlacesList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        places = storage.all(Place).values()
        return [place.to_dict() for place in places]

    @api.expect(place_model)
    @api.response(400, 'Invalid input')
    @api.response(404, 'User not found')
    @api.marshal_with(place_model, code=201)
    def post(self):
        data = request.get_json()
        
        if not data or 'user_id' not in data or 'name' not in data:
            api.abort(400, "user_id and name are required")
            
        if not storage.get(User, data['user_id']):
            api.abort(404, "User not found")
            
        if 'amenity_ids' in data:
            for amenity_id in data['amenity_ids']:
                if not storage.get(Amenity, amenity_id):
                    api.abort(404, f"Amenity {amenity_id} not found")
        
        place = Place(**data)
        place.save()
        return place.to_dict(), 201

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = storage.get(Place, place_id)
        if not place:
            api.abort(404, "Place not found")
        return place.to_dict()

    @api.expect(place_model)
    @api.marshal_with(place_model)
    @api.response(400, 'Invalid input')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        place = storage.get(Place, place_id)
        if not place:
            api.abort(404, "Place not found")
            
        data = request.get_json()
        if not data:
            api.abort(400, "No data provided")
            
        if 'user_id' in data and not storage.get(User, data['user_id']):
            api.abort(404, "User not found")
            
        if 'amenity_ids' in data:
            for amenity_id in data['amenity_ids']:
                if not storage.get(Amenity, amenity_id):
                    api.abort(404, f"Amenity {amenity_id} not found")
        
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(place, key, value)
        
        place.save()
        return place.to_dict()

    @api.route('/<place_id>/reviews')
    class PlaceReviews(Resource):
        @api.marshal_list_with(review_model)
        @api.response(404, 'Place not found')
        def get(self, place_id):
            place = storage.get(Place, place_id)
            if not place:
                api.abort(404, "Place not found")
        
            reviews = [review.to_dict() for review in storage.all(Review).values() 
                 if review.place_id == place_id]
            return reviews
