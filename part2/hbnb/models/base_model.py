from datetime import datetime
import uuid
from hbnb.models.engine.storage import storage

class BaseModel:
    """Clase base que contiene funcionalidad común"""
    def __init__(self, **kwargs):
        """Inicialización con valores por defecto"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        """Actualiza el timestamp y guarda en storage"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convierte el objeto a diccionario"""
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict

    def __str__(self):
        """Representación de cadena del objeto"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
