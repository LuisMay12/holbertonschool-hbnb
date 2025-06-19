from .base_model import BaseModel
import re

class User(BaseModel):
    """Modelo de usuario con validaciones estrictas"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        self.email = kwargs.get('email', '')
        self.is_admin = kwargs.get('is_admin', False)
        
        # Validaciones iniciales
        self.validate()

    def validate(self):
        """Valida los atributos requeridos"""
        if not all([self.first_name, self.last_name, self.email]):
            raise ValueError("First name, last name, and email are required")
        
        if len(self.first_name) > 50 or len(self.last_name) > 50:
            raise ValueError("Names must be ≤ 50 characters")
            
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Invalid email format")

    @property
    def full_name(self) -> str:
        """Nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}"
