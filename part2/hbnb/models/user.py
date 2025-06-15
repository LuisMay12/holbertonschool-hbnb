from hbnb.models.base_model import BaseModel

class User(BaseModel):
    """Clase Usuario del sistema"""
    def __init__(self, **kwargs):
        """Inicialización con atributos específicos"""
        super().__init__(**kwargs)
        self.email = kwargs.get('email', '')
        self.password = kwargs.get('password', '')
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')

    def validate(self):
        """Validación de atributos del usuario"""
        if not isinstance(self.email, str) or '@' not in self.email:
            raise ValueError("Invalid email format")
        if not isinstance(self.password, str) or len(self.password) < 6:
            raise ValueError("Password must be at least 6 characters")
