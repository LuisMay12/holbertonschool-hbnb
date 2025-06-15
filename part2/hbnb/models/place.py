from hbnb.models.base_model import BaseModel

class Place(BaseModel):
    """Clase Lugar/Alojamiento"""
    def __init__(self, **kwargs):
        """Inicialización con atributos específicos"""
        super().__init__(**kwargs)
        self.user_id = kwargs.get('user_id', '')
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.number_rooms = kwargs.get('number_rooms', 0)
        self.number_bathrooms = kwargs.get('number_bathrooms', 0)
        self.max_guest = kwargs.get('max_guest', 0)
        self.price_by_night = kwargs.get('price_by_night', 0)
        self.latitude = kwargs.get('latitude', 0.0)
        self.longitude = kwargs.get('longitude', 0.0)
        self.amenity_ids = kwargs.get('amenity_ids', [])

    def validate(self):
        """Validación de atributos del lugar"""
        if not isinstance(self.name, str) or len(self.name) < 1:
            raise ValueError("Name must be a non-empty string")
        if not isinstance(self.price_by_night, int) or self.price_by_night < 0:
            raise ValueError("Price must be a positive integer")
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
