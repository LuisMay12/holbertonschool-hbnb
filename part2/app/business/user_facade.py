from datetime import datetime
from models.user import User

class HBnBFacade:
    def __init__(self, storage):
        self._storage = storage

    def get_all_users(self):
        return list(self._storage.all(User).values())

    def get_user(self, user_id):
        return self._storage.get(User, user_id)

    def get_user_by_email(self, email):
        users = self._storage.all(User)
        for user in users.values():
            if user.email == email:
                return user
        return None

    def create_user(self, first_name, last_name, email, password):
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        self._storage.add(user)
        return user

    def update_user(self, user_id, **kwargs):
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)
        user.updated_at = datetime.utcnow()
        return user
