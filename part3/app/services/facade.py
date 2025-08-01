from app.persistence.repository import InMemoryRepository # Issue with app, the program doesn't find app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
# from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository

class HBNBFacade:
    """
    Facade principal para el sistema HBnB que centraliza el acceso a:
    - Users (usuarios)
    - Places (alojamientos)
    - Reviews (reseñas)
    - Amenities (comodidades)
    """
    def __init__(self):
        # self.user_repo = SQLAlchemyRepository(User)
        self.user_repo = UserRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ==================== USER METHODS ====================
    def list_users(self):
        """List all users (without sensitive data)"""
        return self.user_repo.get_all()
    
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user) # Task 07
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id) # Task 07
    
    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email) # Task 07

    # def create_user(self, email, first_name, last_name, password='', is_admin=False):
    #     """Create new user with validation"""
    #     if self.user_repo.get_by_attribute('email', email):
    #         raise ValueError("Email is already in use")

    #     user = User(
    #     email=email,
    #     first_name=first_name,
    #     last_name=last_name,
    #     password=password,  # Will be hashed later
    #     is_admin=is_admin
    #     )
    #     self.user_repo.add(user)
    #     return user
    #     # Only allows updated fields
    #     # allowed_fields = ['email', 'first_name', 'last_name', 'is_admin']
    #     # updates = {k: v for k, v in kwargs.items() if k in allowed_fields and v is not None}
    #     # user.update(updates)
    #     # self.user_repo.update(user.id, user.__dict__) 

    # def get_user(self, user_id):
    #     """Obtiene un usuario por ID"""
    #     return self.user_repo.get(user_id)

    # def get_user_by_email(self, email):
    #     """Obtiene un usuario por email"""
    #     return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, **kwargs):
        """Actualiza atributos de un usuario"""
        user = self.user_repo.get(user_id)
        if user:
            user.update(kwargs)
            self.user_repo.update(user.id, user.__dict__)
        else:
            raise ValueError("User not found")	

    # ==================== PLACE METHODS ====================
    def create_place(self, place_data):
        """Crea un nuevo lugar con validación de datos y relaciones"""
        owner_id = place_data.get('owner_id')
        if not self.user_repo.get(owner_id):
            raise ValueError("Owner (user) does not exist")

        # Amenities validation
        amenity_ids = place_data.get("amenities", [])
        for aid in amenity_ids:
            if not self.amenity_repo.get(aid):
                raise ValueError(f"Amenity {aid} does not exist")

        try:
            place = Place(
                title=place_data.get('title'),
                description=place_data.get('description', ''),
                price=place_data.get('price'),
                latitude=place_data.get('latitude'),
                longitude=place_data.get('longitude'),
                owner_id=owner_id,
                amenity_ids=amenity_ids
            )
            self.place_repo.add(place)
            return place
        except Exception as e:
            raise ValueError(str(e))


    def get_place(self, place_id):
        """Devuelve un lugar con owner y amenities anidados"""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # owner
        place.owner = self.user_repo.get(place.owner_id)

        # nest amenities
        place.amenities = [
            self.amenity_repo.get(aid) for aid in getattr(place, 'amenity_ids', [])
            if self.amenity_repo.get(aid)
        ]
        return place


    def get_all_places(self):
        """Devuelve todos los lugares con owner y amenities anidados"""
        places = self.place_repo.get_all()
        for place in places:
            place.owner = self.user_repo.get(place.owner_id)
            place.amenities = [
                self.amenity_repo.get(aid) for aid in getattr(place, 'amenity_ids', [])
                if self.amenity_repo.get(aid)
            ]
        return places

    
    def update_place(self, place_id, place_data):
        """Actualiza campos propios de un lugar (sin amenities)"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        allowed_fields = ['title', 'description', 'price', 'latitude', 'longitude', 'owner_id']
        updates = {k: v for k, v in place_data.items() if k in allowed_fields and v is not None}

        if 'price' in updates and updates['price'] < 0:
            raise ValueError("Invalid price")
        if 'latitude' in updates and not (-90 <= updates['latitude'] <= 90):
            raise ValueError("Invalid latitude")
        if 'longitude' in updates and not (-180 <= updates['longitude'] <= 180):
            raise ValueError("Invalid longitude")

        if 'owner_id' in updates and not self.user_repo.get(updates['owner_id']):
            raise ValueError("Owner not found")

        # Apply changes
        for key, value in updates.items():
            setattr(place, key, value)
        
        place.validate()

        self.place_repo.update(place.id, place.__dict__)
        return place


    def delete_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        self.place_repo.delete(place_id)
        self.place_repo.save()


    # def get_places_by_user(self, user_id): # maybe it is not needed
    #     """Obtiene todos los alojamientos de un usuario"""
    #     return [p for p in self.place_repo.get_all() if p.user_id == user_id]


   	# ==================== REVIEW METHODS ====================
    def create_review(self, review_data):
        """Creates a new review with validation for user and place existence"""
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        text = review_data.get('text')
        rating = review_data.get('rating')

        if not (self.user_repo.get(user_id) and self.place_repo.get(place_id)):
            raise ValueError("User or Place does not exist")

        # Let the model handle validation
        review = Review(
            user_id=user_id,
            place_id=place_id,
            text=text,
            rating=rating
        )

        self.review_repo.add(review)

        # Update place to include the review ID
        place = self.place_repo.get(place_id)
        if not hasattr(place, 'review_ids'):
            place.review_ids = []
        place.review_ids.append(review.id)
        self.place_repo.update(place.id, place.__dict__)

        return review


    def get_review(self, review_id):
        """Retrieves a review by ID"""
        return self.review_repo.get(review_id)


    def get_all_reviews(self):
        """Returns all reviews"""
        return self.review_repo.get_all()


    def get_reviews_by_place(self, place_id):
        """Returns all reviews for a specific place"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return [r for r in self.review_repo.get_all() if r.place_id == place_id]


    def update_review(self, review_id, review_data):
        """Updates text and/or rating of a review"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")

        allowed_fields = ['text', 'rating']
        updates = {k: v for k, v in review_data.items() if k in allowed_fields and v is not None}

        if 'text' in updates:
            review.text = updates['text']
        if 'rating' in updates:
            if not 1 <= updates['rating'] <= 5:
                raise ValueError("Rating must be between 1 and 5")
            review.rating = updates['rating']

        review.validate()
        self.review_repo.update(review.id, review.__dict__)
        return review


    def delete_review(self, review_id):
        """Deletes a review and removes it from the related place"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")

        self.review_repo.delete(review_id)

        # Clean up reference in the place
        place = self.place_repo.get(review.place_id)
        if place and hasattr(place, 'review_ids') and review_id in place.review_ids:
            place.review_ids.remove(review_id)
            self.place_repo.update(place.id, place.__dict__)

	
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
    
    def get_review_by_user_and_place(self, user_id, place_id):
        """Return the review written by a specific user for a specific place, if it exists"""
        all_reviews = self.review_repo.get_all()
        for review in all_reviews:
            if review.user_id == user_id and review.place_id == place_id:
                return review
        return None
    
# Singleton pattern for facade
hbnb_facade = HBNBFacade()
