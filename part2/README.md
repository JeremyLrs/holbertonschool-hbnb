# HBnB - Part 2 — Business Logic & API Implementation

## Overview

This part of the **Holberton School HBnB project** represents the **implementation phase** of the application.
After defining the design and architecture in Part 1, this stage focuses on building the **Business Logic Layer** and the **Presentation Layer (API)** using **Python**, **Flask**, and **flask-restx**.

The goal is to bring the architecture to life by creating a working, modular, and scalable foundation that supports the main entities of the application: **User**, **Place**, **Review**, and **Amenity**.

---

## Objectives

### Project Setup

* Organize the project into **modular layers**:

  * **Presentation Layer** → Flask + flask-restx (API)
  * **Business Logic Layer** → Core models and validation logic
  * **Persistence Layer** → In-memory repository (temporary data store)
* Prepare the **Facade Pattern** to simplify communication between layers.

### Business Logic

* Implement core entities:

  * `User` → represents application users.
  * `Place` → represents listings/locations.
  * `Review` → user feedback for a place.
  * `Amenity` → features available in a place.
* Define relationships between these entities.
* Implement validation rules and helper methods.

### API Development

* Create RESTful endpoints for all entities.
* Implement CRUD operations:

  * **User:** Create, Read, Update (no Delete)
  * **Amenity:** Create, Read, Update (no Delete)
  * **Place:** Create, Read, Update (no Delete)
  * **Review:** Create, Read, Update, Delete
* Use **flask-restx** to generate automatic Swagger documentation.
* Serialize and return related data (e.g. place owner info, amenities list).

### Testing & Validation

* Validate request payloads and responses.
* Test endpoints using **Postman** or **cURL**.
* Write unit tests for business logic and API routes.

---

## Project Structure

```
part2/
│
├── app.py                      # Application entry point
│
├── presentation/               # Flask REST API (flask-restx)
│   ├── __init__.py
│   ├── routes/
│   │   ├── users.py
│   │   ├── amenities.py
│   │   ├── places.py
│   │   └── reviews.py
│   └── api_factory.py          # API namespace setup
│
├── business/                   # Core business logic classes
│   ├── __init__.py
│   ├── user.py
│   ├── place.py
│   ├── review.py
│   └── amenity.py
│
├── persistence/                # In-memory repository (temporary)
│   ├── __init__.py
│   └── repository.py
│
├── facade/                     # Facade connecting API and business logic
│   └── hbnb_facade.py
│
├── tests/                      # Unit and integration tests
│
└── README.md
```

---

## How to Run the Application

### 1. Install Dependencies

```bash
pip install flask flask-restx
```

### 2. Run the Server

```bash
python3 app.py
```

### 3. Access the API

* Base URL: [http://localhost:5000/api/v1/](http://localhost:5000/api/v1/)

---

## Example Requests

### Create a User

```bash
curl -X POST http://localhost:5000/api/v1/users \
-H "Content-Type: application/json" \
-d '{"first_name": "Alice", "last_name": "Smith", "email": "alice@example.com"}'
```

### Get All Users

```bash
curl http://localhost:5000/api/v1/users
```

### Update a Place

```bash
curl -X PUT http://localhost:5000/api/v1/places/<place_id> \
-H "Content-Type: application/json" \
-d '{"name": "Beach House", "price": 250}'
```

---

## Key Concepts

| Concept                   | Description                                                                            |
| ------------------------- | -------------------------------------------------------------------------------------- |
| **In-Memory Persistence** | Temporary storage system that mimics database operations using Python data structures. |
| **Facade Pattern**        | Simplifies interaction between API and business logic layers.                          |
| **Flask-RESTx**           | Extension for building and documenting RESTful APIs.                                   |
| **Modular Architecture**  | Separates concerns into distinct layers for scalability and maintainability.           |
| **Data Serialization**    | Converts Python objects into JSON for API responses.                                   |

---

## Technologies Used

| Tool                     | Purpose                            |
| ------------------------ | ---------------------------------- |
| **Python 3.8+**          | Core programming language          |
| **Flask**                | Web framework                      |
| **Flask-RESTx**          | REST API and Swagger documentation |
| **In-Memory Repository** | Temporary persistence system       |
| **unittest / pytest**    | Testing                            |
| **cURL / Postman**       | API testing tools                  |

---

## Authors

* **Jeremy Laurens**
* **Malik Bouanani**
* **Christophe Barrere**