from .base_model import BaseModel

class Review(BaseModel):
    """Modelo de reseña con validación de rating"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = kwargs.get('text', '')
        self.rating = kwargs.get('rating', 0)
        self.place_id = kwargs.get('place_id', '')  # Relación con Place
        self.user_id = kwargs.get('user_id', '')  # Relación con User
        
        self.validate()

    def validate(self):
        """Valida el rating y texto"""
        if not self.text:
            raise ValueError("Review text is required")
            
        if not 1 <= self.rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
