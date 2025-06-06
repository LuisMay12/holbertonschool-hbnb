# HBnB Architecture - Technical Notes

## Layer-by-Layer Breakdown

### Presentation Layer (APIService)
**Responsibilities**:
- Receives HTTP/HTTPS requests from clients
- Handles JSON serialization/deserialization
- Manages authentication headers
- Returns standardized responses (success/error formats)

**Key Characteristics**:
- Zero business logic
- Stateless by design
- Methods map 1:1 to API endpoints

### Business Logic Layer
**Core Components**:
1. **Facade Controller**:
   - Single entry point from Presentation Layer
   - Routes requests to appropriate entities
   - Enforces cross-entity validation

2. **Domain Entities**:
   - `User`: Handles registration, authentication, profile management
   - `Place`: Manages property listings, pricing rules, availability
   - `Review`: Enforces rating constraints (1-5 stars)
   - `Amenity`: Maintains unique feature identifiers

**Business Rules Implemented**:
- User can't review their own property
- Place price must be ≥ $10 minimum
- Amenity names are case-insensitive unique

### Persistence Layer (DBStorage)
**Abstraction Features**:
- Unified interface for all CRUD operations
- Transactions support
- Cache integration (Redis optional)
- Database-agnostic design

## Facade Pattern Deep Dive

### Why We Chose Facade
1. **Complexity Hiding**:
   ```python
   # Instead of:
   api → User.validate() → Place.validate() → DB.save()

   # We use:
   api → Facade.create_booking()  # Handles all steps
