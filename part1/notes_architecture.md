# HBnB Architecture – Explanatory Notes

## Presentation Layer

The **Presentation Layer** serves as the interface between external users (such as frontend applications or API clients) and the HBnB system. In this diagram, it is represented by the class:

- **APIService**: This class provides methods like `create_resource()`, `get_resource()`, `update_resource()`, and `delete_resource()`, simulating typical RESTful API operations.

This layer **does not handle any business logic directly**. Instead, it delegates all functional requests to the `Facade` class in the Business Logic Layer. Its primary role is to manage user interaction and route incoming requests properly.

---

## Business Logic Layer

The **Business Logic Layer** contains the core functionality and application rules of the HBnB system. It is composed of:

- **Facade**: This class implements the **Facade Pattern**, acting as a unified entry point for all business logic operations. It receives high-level commands from the `APIService` and forwards them to the appropriate internal components.
- **User**, **Place**, **Review**, **Amenity**: These are the core domain entities of the application, encapsulating the behavior and attributes relevant to each concept.

This layer ensures that operations follow the business rules and remains independent from data storage details.

---

## Persistence Layer

The **Persistence Layer** is responsible for storing and retrieving data. In the diagram, it is represented by:

- **DBStorage**: This class abstracts the data storage system and exposes methods like `new()`, `save()`, `delete()`, and `reload()`. It simulates database access or an ORM.

Each business entity (`User`, `Place`, `Review`, `Amenity`) interacts with `DBStorage` to persist changes, retrieve information, or delete records.

---

## Facade Pattern Explanation

The **Facade Pattern** is implemented through the `Facade` class, which acts as a mediator between the presentation and business logic layers. This pattern:

- Simplifies the API layer’s communication with the system’s logic.
- Reduces coupling by allowing the `APIService` to interact with a single interface (`Facade`), rather than directly calling each entity.
- Centralizes control, improving maintainability and allowing validations, workflows, or rules to be handled in one place.

This design promotes a clean separation of concerns and makes the application easier to scale and test.

