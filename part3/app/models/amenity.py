from .base_model import BaseModel

class Amenity(BaseModel):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.name = kwargs.get('name', '')
        
        self.validate()

    def validate(self):
        """Name Validation"""
        if not self.name:
            raise ValueError("Amenity name is required")
            
        if len(self.name) > 50:
            raise ValueError("Name must be ≤ 50 characters")
