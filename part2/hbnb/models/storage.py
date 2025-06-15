from models.user import User
from models.amenity import Amenity

class Storage:
    __objects = {}

    def all(self, cls=None):
        if cls:
            return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
        return self.__objects

    def get(self, cls, id):
        key = f"{cls.__name__}.{id}"
        return self.__objects.get(key)

    def new(self, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        # Implementación de persistencia vendrá después
        pass

storage = Storage()
