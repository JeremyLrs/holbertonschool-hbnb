# HBnB Evolution - Part 1: Technical Documentation

## Context and Objective

The first part of this project consists of creating a complete technical documentation for the **HBnB Evolution** application, a simplified clone of AirBnB.  
This documentation will serve as a foundation for future development and provide an understanding of the overall architecture, detailed business logic design, and interactions between system components.

---

## Problem Description

The HBnB Evolution application allows users to:

- **User Management**: Sign up, update their profile, and be identified as regular users or administrators.
    
- **Place Management**: Create property listings with name, description, price, location (latitude/longitude), and a list of amenities.
    
- **Review Management**: Leave comments and ratings on visited places.
    
- **Amenity Management**: Add, edit, and list the amenities associated with places.
    

Each entity has a unique identifier and records creation and update timestamps.

---

## Architecture and Layers

The application follows a **layered architecture**:

1. **Presentation Layer**: User interface, services, and API.
    
2. **Business Logic Layer**: Models and business logic (User, Place, Review, Amenity).
    
3. **Persistence Layer**: Database access and data storage.
    

Communication between layers is implemented via the **Facade Pattern** to simplify interactions.

---

## Tasks and Deliverables

### 1. High-Level Package Diagram

- Goal: Create a package diagram illustrating the three-layer architecture and the communication path via the **Facade Pattern**.  
- Deliverable: UML diagram with explanations of each layer’s responsibilities.

---

### 2. Detailed Class Diagram (Business Logic Layer)

- Goal: Detail the main entities with their attributes, methods, and relationships.  
- Entities: `User`, `Place`, `Review`, `Amenity`.  
- Relationships: Associations, compositions, inheritance, and multiplicities.  
- Deliverable: UML class diagram with explanatory notes on each entity and their relationships.

---

### 3. Sequence Diagrams for API Calls

- Goal: Illustrate interaction between layers for four API calls:
    
    1. User registration  
    2. Place creation  
    3. Review submission  
    4. Retrieval of a list of places  
    
- Deliverable: UML sequence diagrams with explanatory notes.

---

### 4. Documentation Compilation

- Goal: Compile all diagrams and explanatory notes into a complete technical document.  
- Contents:
    
    - Introduction  
    - General architecture  
    - Business Logic Layer (class diagram)  
    - API Interaction Flow (sequence diagrams)  
    - Explanatory notes for each diagram  

---

## Recommendations

- Use **Mermaid.js** to generate and maintain diagrams.  
- Ensure **consistency** in terminology and UML notation.  
- Clearly document all design decisions.  
- Proofread and validate diagrams to ensure accuracy before final compilation.  

---

## GitHub Repository

- **Repository**: `holbertonschool-hbnb`  
- **Directory**: `part1`
# Part 1
