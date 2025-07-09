from .base_model import BaseModel
from app import bcrypt
import re

class User(BaseModel):
    """User model with strict validations"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        self.email = kwargs.get('email', '')
        self.is_admin = kwargs.get('is_admin', False)
        password = kwargs.get('password')
        if password:
            self.hash_password(password)
        else:
            self.password = ''

        
        # Initials validations
        self.validate()

    def validate(self):
        """Validates the required attributes"""
        if not all([self.first_name, self.last_name, self.email]):
            raise ValueError("First name, last name, and email are required")
        
        if len(self.first_name) > 50 or len(self.last_name) > 50:
            raise ValueError("Names must be ≤ 50 characters")
            
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Invalid email format")
    
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)


    @property
    def full_name(self) -> str:
        """User full name"""
        return f"{self.first_name} {self.last_name}"
