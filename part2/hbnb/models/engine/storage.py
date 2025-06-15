class Storage:
    """Clase de almacenamiento en memoria"""
    __objects = {}

    def all(self, cls=None):
        """Retorna todos los objetos o los de una clase específica"""
        if cls:
            return {k: v for k, v in self.__objects.items() 
                   if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """Agrega un nuevo objeto al almacenamiento"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Persiste los objetos (implementación dummy para memoria)"""
        pass

    def delete(self, obj=None):
        """Elimina un objeto del almacenamiento"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]

storage = Storage()
