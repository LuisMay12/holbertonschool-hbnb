from hbnb.models.base_model import BaseModel

class Amenity(BaseModel):
    """Clase Comodidad/Servicio"""
    def __init__(self, **kwargs):
        """Inicialización con atributos específicos"""
        super().__init__(**kwargs)
        self.name = kwargs.get('name', '')

    def validate(self):
        """Validación de atributos de la comodidad"""
        if not isinstance(self.name, str) or len(self.name) < 1:
            raise ValueError("Amenity name cannot be empty")
