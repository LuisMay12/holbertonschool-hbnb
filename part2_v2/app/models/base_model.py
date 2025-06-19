import uuid
from datetime import datetime
from typing import Dict, Any

class BaseModel:
    """Clase base con UUID y manejo de timestamps"""
    
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
        """Actualiza el timestamp de modificación"""
        self.updated_at = datetime.now()

    def update(self, data: Dict[str, Any]):
        """Actualiza atributos con validación"""
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
