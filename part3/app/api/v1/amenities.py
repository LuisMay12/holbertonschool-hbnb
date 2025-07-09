from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade

api = Namespace('Amenities', description='Amenities operations', path='/amenities')

# Swagger documentation model
amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='ID único'),
    'name': fields.String(required=True, description='Nombre de la comodidad', max_length=50)
})

@api.route('/')
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List of all amenities"""
        return hbnb_facade.get_all_amenities()

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    @api.response(400, 'Nombre inválido o duplicado')
    def post(self):
        """Register a new amenity"""
        data = api.payload
        
        # Validación de nombre único
        existing = next((a for a in hbnb_facade.get_all_amenities() if a.name.lower() == data['name'].lower()), None)
        if existing:
            api.abort(400, 'Ya existe una comodidad con este nombre')
            
        try:
            amenity = hbnb_facade.create_amenity(data['name'])
            return amenity, 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    @api.response(404, 'Comodidad no encontrada')
    def get(self, amenity_id):
        """Retrieve an amenity by ID"""
        amenity = hbnb_facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, 'Comodidad no encontrada')
        return amenity

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    @api.response(400, 'Nombre inválido')
    @api.response(404, 'Comodidad no encontrada')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = api.payload
        try:
            hbnb_facade.update_amenity(
                amenity_id=amenity_id,
                name=data['name']
            )
            return hbnb_facade.get_amenity(amenity_id)
        except ValueError as e:
            api.abort(400, str(e))
