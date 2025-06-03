```mermaid
classDiagram
    %% Base class
    class BaseModel {
        +str id
        +datetime created_at
        +datetime updated_at
        +save()
        +to_dict()
    }

    %% User class
    class User {
        +str email
        +str password
        +str first_name
        +str last_name
    }

    %% Place class
    class Place {
        +str name
        +str description
        +int number_rooms
        +int number_bathrooms
        +int max_guest
        +int price_by_night
        +float latitude
        +float longitude
        +str city_id
        +str user_id
    }

    %% Review class
    class Review {
        +str text
        +str user_id
        +str place_id
    }

    %% Amenity class
    class Amenity {
        +str name
    }

    %% Relationships
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    User "1" --> "0..*" Place : owns
    Place "1" --> "0..*" Review : has
    User "1" --> "0..*" Review : writes
    Place "1" --> "0..*" Amenity : has (many-to-many)
```
