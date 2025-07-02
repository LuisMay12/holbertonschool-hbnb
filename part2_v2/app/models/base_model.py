from app import db
import uuid
from datetime import datetime
from typing import Dict, Any

class BaseModel(db.Model):
    __abstract__ = True # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, *args, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        if kwargs:
            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at']:
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                setattr(self, key, value)

    def save(self):
        """Update the modification timestamp"""
        self.updated_at = datetime.now()

    def update(self, data: Dict[str, Any]):
        """Update attributes with validation"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self) -> Dict[str, Any]:
        """Serializa el objeto a diccionario"""
        result = self.__dict__.copy()
        result['__class__'] = self.__class__.__name__
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        return result
