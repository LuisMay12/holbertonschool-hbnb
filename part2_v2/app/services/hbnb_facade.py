from app.persistence.in_memory_repo import InMemoryRepository

class HBNBFacade:
    def __init__(self):
        self.repo = InMemoryRepository()

    def list_all(self):
        return self.repo.get_all()

    def add(self, obj):
        self.repo.save(obj)
