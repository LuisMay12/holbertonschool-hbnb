from hbnb.models.base_model import BaseModel

class Review(BaseModel):
    """Clase Reseña/Comentario"""
    def __init__(self, **kwargs):
        """Inicialización con atributos específicos"""
        super().__init__(**kwargs)
        self.place_id = kwargs.get('place_id', '')
        self.user_id = kwargs.get('user_id', '')
        self.text = kwargs.get('text', '')

    def validate(self):
        """Validación de atributos de la reseña"""
        if not isinstance(self.text, str) or len(self.text) < 1:
            raise ValueError("Review text cannot be empty")
        if not self.place_id:
            raise ValueError("Review must be associated with a place")
        if not self.user_id:
            raise ValueError("Review must be associated with a user")
