# HBnB Project - Part 2: Implementation of Business Logic and API Endpoints

## Overview

This phase focuses on the implementation of the core layers of the HBnB application using **Python**, **Flask**, and **Flask-RESTx**. Based on the architectural design from Part 1, this part includes setting up the project structure, implementing the business logic, defining RESTful API endpoints, and preparing for integration with future features such as authentication and persistent storage.

---

## Objectives

By the end of this part, the following outcomes should be achieved:

- Set up a modular and scalable project structure.
- Implement core business logic classes: `User`, `Place`, `Review`, and `Amenity`.
- Apply the **Facade design pattern** to coordinate communication between layers.
- Define and implement RESTful API endpoints using Flask and Flask-RESTx.
- Handle serialization, nested relationships, and proper validation of input data.
- Test and validate all endpoints via cURL and Swagger UI.

---

## Project Structure

```
part2/
├── app/
│   ├── api/
│   │   └── routes.py                   # API Endpoints (Presentation Layer)
│   ├── persistence/
│   │   └── models/
│   │       ├── base_model.py          # Base class for common attributes
│   │       └── in_memory_repo.py      # In-memory data repository
│   └── services/
│       └── hbnb_facade.py             # Facade Pattern Implementation (Business Logic)
├── main.py                            # Application bootstrap
├── run.py                             # Flask app runner
└── README.md
```

---

## Key Concepts

### Business Logic Implementation
- Entities include necessary attributes (e.g., `id`, `created_at`, `updated_at`) and domain-specific behaviors.
- Relationships: 
  - User owns Places
  - Places have Amenities
  - Places and Reviews are linked
  - User writes Reviews

### RESTful API Design
- Endpoints follow standard REST conventions.
- CRUD operations implemented:
  - Users: `POST`, `GET`, `PUT`
  - Amenities: `POST`, `GET`, `PUT`
  - Places: `POST`, `GET`, `PUT`
  - Reviews: `POST`, `GET`, `PUT`, `DELETE`

### Facade Pattern
- The `hbnb_facade.py` module simplifies the interface between the API and the business logic by centralizing service access.

### Data Serialization
- Extended responses include nested fields, such as:
  - When retrieving a Place, include `owner.first_name`, `owner.last_name`, and a list of `amenities`.

---

## Testing and Validation

- Manual testing using `cURL` and Swagger UI
- Input validation and error handling
- Black-box testing of endpoints
- Tests documented in the testing report

---

## Tech Stack

- Python 3.10+
- Flask
- Flask-RESTx
- UUID4 for unique IDs
- In-memory repository (to be replaced with SQLAlchemy in Part 3)

---

## Next Steps (Part 3 Preview)

- Integrate SQLAlchemy as the full persistence layer.
- Implement JWT-based authentication.
- Add role-based access control (admin vs regular users).

---

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [Flask-RESTx Docs](https://flask-restx.readthedocs.io/en/latest/)
- [RESTful API Design](https://restfulapi.net/)
- [Facade Pattern](https://refactoring.guru/design-patterns/facade/python/example)
