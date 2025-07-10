from .base_model import BaseModel
from app import db

class Amenity(db.Model):
    __tablename__ = 'amenities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    
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
