from .base_model import BaseModel
from typing import List
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(db.Model):
    __tablename__ = 'places'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, backref=db.backref('places', lazy=True))
    """Place model with geospatial relationships and validations"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.price = kwargs.get('price', 0.0)
        self.latitude = kwargs.get('latitude', 0.0)
        self.longitude = kwargs.get('longitude', 0.0)
        self.owner_id = kwargs.get('owner_id', '')  # Relación con User
        self.amenity_ids: List[str] = kwargs.get('amenity_ids', [])  # Many-to-many
        self.review_ids: List[str] = kwargs.get('review_ids', [])  # One-to-many
        
        self.validate()

    def validate(self):
        """Validates attributes"""
        if not self.title:
            raise ValueError("Title is required")

        if len(self.title) > 100:
            raise ValueError("Title must be ≤ 100 characters")
            
        if self.price < 0:
            raise ValueError("Price must be positive")
            
        if not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
            
        if not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

    def add_amenity(self, amenity_id: str):
        """Añade una comodidad"""
        if amenity_id not in self.amenity_ids:
            self.amenity_ids.append(amenity_id)
            self.save()
