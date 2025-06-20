from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBNBFacade:
    """
    Facade principal para el sistema HBnB que centraliza el acceso a:
    - Users (usuarios)
    - Places (alojamientos)
    - Reviews (reseñas)
    - Amenities (comodidades)
    """
    
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ==================== USER METHODS ====================
    def list_users(self):
        """List all users (without sensitive data)"""
        return self.user_repo.get_all()

    def create_user(self, email, first_name, last_name, password='', is_admin=False):
        """Create new user with validation"""
        if self.user_repo.get_by_attribute('email', email):
            raise ValueError("Email is already in use")

        user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,  # Will be hashed later
        is_admin=is_admin
        )
        self.user_repo.add(user)
        return user
        # Solo actualiza campos permitidos
        allowed_fields = ['email', 'first_name', 'last_name', 'is_admin']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields and v is not None}
        user.update(updates)
        self.user_repo.update(user.id, user.__dict__) 

    def get_user(self, user_id):
        """Obtiene un usuario por ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Obtiene un usuario por email"""
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, **kwargs):
        """Actualiza atributos de un usuario"""
        user = self.user_repo.get(user_id)
        if user:
            user.update(kwargs)
            self.user_repo.update(user.id, user.__dict__)
        else:
            raise ValueError("User not found")	

    # ==================== PLACE METHODS ====================
    def create_place(self, user_id, name, description, **kwargs):
        """Crea un nuevo alojamiento"""

        if not (self.user_repo.get(user_id)):
            raise ValueError("Owner (user) does not exist")
        
        place = Place(
            user_id=user_id,
            name=name,
            description=description,
            **kwargs
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Obtiene un alojamiento por ID"""
        return self.place_repo.get(place_id)

    def get_places_by_user(self, user_id):
        """Obtiene todos los alojamientos de un usuario"""
        return [p for p in self.place_repo.get_all() if p.user_id == user_id]

   	# ==================== REVIEW METHODS ====================
    def create_review(self, user_id, place_id, text, rating):
        """Crea una nueva reseña con validación de relaciones"""
        # Validación de existencia
        if not (self.user_repo.get(user_id) and self.place_repo.get(place_id)):
            raise ValueError("User or Place does not exist")
    
        # Validación de rating
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")

        review = Review(
            user_id=user_id,
            place_id=place_id,
            text=text,
            rating=rating
        )
        self.review_repo.add(review)
    
        place = self.place_repo.get(place_id)
        if not hasattr(place, 'review_ids'):
            place.review_ids = []
    
        place.review_ids.append(review.id)
        self.place_repo.update(place.id, place.__dict__)
        return review

    def get_reviews_for_place(self, place_id):
        """Obtiene reseñas de un alojamiento (mantener existente)"""
        return [r for r in self.review_repo.get_all() if r.place_id == place_id] 
	
    # ==================== AMENITY METHODS ====================
    def create_amenity(self, name):
        """Creates a new amenity with validation"""
        if not name or len(name) > 50:
            raise ValueError("Name must be between 1 and 50 characters")
    
        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Gets an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Lists all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, name):
        """Updates an existing amenity"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
    
        if not name or len(name) > 50:
            raise ValueError("Name must be between 1 and 50 characters")
    
        amenity.name = name
        self.amenity_repo.update(amenity.id, amenity.__dict__)
# Singleton pattern para el facade
hbnb_facade = HBNBFacade()
