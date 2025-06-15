from models.engine.storage import storage

class BaseService:
    @classmethod
    def get_all(cls, model_cls):
        return storage.all(model_cls)

    @classmethod
    def get_by_id(cls, model_cls, obj_id):
        return storage.get(model_cls, obj_id)

    @classmethod
    def create(cls, model_cls, **kwargs):
        obj = model_cls(**kwargs)
        storage.new(obj)
        storage.save()
        return obj
