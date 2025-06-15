from hbnb.models.user import User
from hbnb.models.engine.storage import storage

class UserService:
    @staticmethod
    def create_user(data):
        """Crea un nuevo usuario"""
        if not data or 'email' not in data or 'password' not in data:
            return None, "Email and password are required", 400
            
        user = User(**data)
        user.save()
        return user, None, 201

    @staticmethod
    def get_user(user_id):
        """Obtiene un usuario por ID"""
        user = storage.get(User, user_id)
        if not user:
            return None, "User not found", 404
        return user, None, 200

    @staticmethod
    def get_all_users():
        """Obtiene todos los usuarios"""
        users = list(storage.all(User).values())
        return users, None, 200

    @staticmethod
    def update_user(user_id, data):
        """Actualiza un usuario existente"""
        user = storage.get(User, user_id)
        if not user:
            return None, "User not found", 404
            
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return user, None, 200
