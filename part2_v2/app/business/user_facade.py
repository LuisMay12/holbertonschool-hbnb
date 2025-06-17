from app.persistence.in_memory_repo import InMemoryRepository
from app.persistence.user import User

class UserFacade:
    def __init__(self):
        self.repo = InMemoryRepository()

    def create_user(self, data):
        user = User(
            email=data.get("email"),
            password=data.get("password"),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", "")
        )
        
        self.repo.save("User", user)
        return user

    def get_user(self, user_id):
        return self.repo.get("User", user_id)

    def get_all_users(self):
        return self.repo.all("User")

    def update_user(self, user_id, updates):
        user = self.repo.get("user", user_id)
        if not user:
            return None
        for key in ["fist_name", "last_name", "email", "password"]:
            if key in updates:
                setattr(user, key, updates[key])
        user.update_timestamp()
        return user
