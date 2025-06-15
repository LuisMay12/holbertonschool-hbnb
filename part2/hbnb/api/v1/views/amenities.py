from flask import request
from flask_restx import Resource, Namespace, fields
from models.amenity import Amenity
from models.engine.storage import storage

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True)
})

@api.route('/')
class AmenitiesList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        amenities = storage.all(Amenity).values()
        return [amenity.to_dict() for amenity in amenities]

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        data = request.get_json()
        if not data or 'name' not in data:
            api.abort(400, "Name is required")
        amenity = Amenity(**data)
        amenity.save()
        return amenity.to_dict(), 201

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity.to_dict()

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        
        data = request.get_json()
        if not data:
            api.abort(400, "No data provided")
        
        if 'name' in data:
            amenity.name = data['name']
        
        amenity.save()
        return amenity.to_dict()
