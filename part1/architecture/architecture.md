# HBnB Evolution - Architecture Diagram

## Three-Layer System Design

```mermaid
classDiagram
    %% ===== Presentation Layer =====
    class APIService {
        <<Interface>>
        +register_user()
        +create_place()
        +add_review()
        +list_places()
    }

    %% ===== Business Logic Layer =====
    class Facade {
        +handle_user_creation()
        +validate_place_data()
        +process_review()
        +filter_places()
    }
    
    class User
    class Place
    class Review
    class Amenity

    %% ===== Persistence Layer =====
    class DBStorage {
        +save()
        +get()
        +delete()
        +update()
    }

    %% ===== Relationships =====
    APIService --> Facade : "1. Requests via\nFacade Pattern"
    Facade --> User : "2. Delegates to\nBusiness Entities"
    Facade --> Place
    Facade --> Review
    Facade --> Amenity
    User --> DBStorage : "3. Persists data"
    Place --> DBStorage
    Review --> DBStorage
    Amenity --> DBStorage
