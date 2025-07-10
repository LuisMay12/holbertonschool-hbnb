import uuid
from datetime import datetime
from typing import Dict, Any
from app import db

class BaseModel(db.Model):
    __abstract__ = True # The new changes

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def update(self, data: Dict[str, Any]):
        """Update attributes with validation"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def save(self):
        """Save the model and commit changes"""
        db.session.add(self)
        db.session.commit()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the object to a dictionary"""
        result = {k: v for k, v in self.__dict__.items() if not k.startswith('_sa_instance_state')}
        result['__class__'] = self.__class__.__name__
        result['created_at'] = self.created_at.isoformat() if self.created_at else None
        result['updated_at'] = self.updated_at.isoformat() if self.updated_at else None
        return result
