from .base_model import BaseModel
from app import bcrypt, db
import re
from sqlalchemy.orm import validates

class User(BaseModel):
    __tablename__ = 'users' # New changes

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
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
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    @property
    def full_name(self) -> str:
        """User full name"""
        return f"{self.first_name} {self.last_name}"
    
    
    """Use this later for validation to keep the code clean and organized"""
    
    # @validates('email')
    # def validate_email(self, key, value):
    #     if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
    #         raise ValueError("Invalid email format")
    #     return value

    # @validates('first_name', 'last_name')
    # def validate_name(self, key, value):
    #     if not value:
    #         raise ValueError(f"{key} is required")
    #     if len(value) > 50:
    #         raise ValueError(f"{key} must be 50 characters or fewer")
    #     return value
