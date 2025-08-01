from .base_model import BaseModel
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    """Review template with rating validation"""
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.text = kwargs.get('text', '')
        self.rating = kwargs.get('rating', 0)
        self.place_id = kwargs.get('place_id', '')
        self.user_id = kwargs.get('user_id', '')
        
        self.validate()

    def validate(self):
        """Validate the rating and text"""
        if not self.text:
            raise ValueError("Review text is required")
            
        if not 1 <= self.rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
