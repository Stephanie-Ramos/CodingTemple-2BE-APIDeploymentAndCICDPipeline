# Advanced Mechanic Shop API

## Project Overview

The Advanced Mechanic Shop API is a RESTful backend application built with **Flask**, **SQLAlchemy**, **Marshmallow**, and **MySQL**. This project expands upon the original Mechanic Shop API by implementing advanced backend features including JWT authentication, rate limiting, caching, advanced database queries, pagination, and inventory management.

The API allows users to manage customers, mechanics, service tickets, and inventory while demonstrating secure authentication, many-to-many relationships, and modern API development practices.

---

## Features

### Customer Management
- Create a customer
- Retrieve all customers
- Retrieve a customer by ID
- Update customer information
- Delete a customer

### Customer Authentication
- Customer Login using email and password
- JSON Web Token (JWT) generation
- Protected routes using Bearer Token authentication
- Retrieve only the authenticated customer's service tickets

### Mechanic Management
- Create mechanic
- Retrieve all mechanics
- Retrieve mechanic by ID
- Update mechanic
- Delete mechanic
- Retrieve mechanics ordered by number of completed service tickets

### Service Ticket Management
- Create service ticket
- Retrieve all service tickets
- Retrieve service ticket by ID
- Update service ticket
- Delete service ticket
- Assign mechanics to service tickets
- Add and remove mechanics from existing service tickets

### Inventory Management
- Create inventory parts
- Retrieve all inventory parts
- Retrieve inventory part by ID
- Update inventory parts
- Delete inventory parts
- Assign inventory parts to service tickets

---

## Advanced Features

### JWT Authentication
- Secure customer login
- Bearer Token authorization
- Protected API endpoints
- Customer-specific ticket retrieval

### Rate Limiting
Implemented using **Flask-Limiter** to protect sensitive endpoints from abuse.

Example:
- Customer Login
- Customer retrieval routes

---

### Caching
Implemented using **Flask-Caching** to reduce unnecessary database queries for frequently requested data.

Example:
- Mechanics GET endpoint

---

### Advanced SQLAlchemy Queries
- Mechanics ranked by number of completed service tickets
- Add/remove mechanics from service tickets
- Customer pagination

---

### Pagination
Customer records support pagination using query parameters.

Example:

```
GET /customers?page=1&per_page=5
```

---

### Many-to-Many Relationships

#### Service Tickets ↔ Mechanics

A service ticket may have multiple mechanics.

A mechanic may work on multiple service tickets.

#### Service Tickets ↔ Inventory

A service ticket may require multiple inventory parts.

An inventory part may be used on multiple service tickets.

---

## Technologies Used

- Python 3.12
- Flask
- SQLAlchemy
- Marshmallow
- Flask-Limiter
- Flask-Caching
- python-jose (JWT)
- MySQL
- MySQL Connector
- Postman
- Git
- GitHub

---

## Project Structure

```
project/
│
├── application/
│   ├── blueprints/
│   │   ├── customers/
|   |      |__ __init__.py
|   |      |__ routes.py
|   |      |__ schemas.py
|   |
│   │   ├── mechanics/
│   │   ├── service_tickets/
│   │   └── inventory/
│   │
│   ├── extensions.py
│   ├── models.py
│   └── __init__.py
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
└── Mechanic_Shop_API.postman_collection.json
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

### Navigate into the project

```bash
cd YOUR_REPOSITORY
```

### Create a virtual environment

Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
SQLALCHEMY_DATABASE_URI=mysql+mysqlconnector://USERNAME:PASSWORD@localhost/mechanic_shop_db
SECRET_KEY=your_secret_key_here
```

---

## Run the Application

```bash
python app.py
```

The API will be available at:

```
http://127.0.0.1:5001
```

---

## Example Endpoints

### Customers

| Method | Endpoint |
|---------|----------|
| POST | /customers |
| GET | /customers |
| GET | /customers/<id> |
| PUT | /customers/<id> |
| DELETE | /customers/<id> |
| POST | /customers/login |
| GET | /customers/my-tickets |

---

### Mechanics

| Method | Endpoint |
|---------|----------|
| POST | /mechanics |
| GET | /mechanics |
| GET | /mechanics/<id> |
| PUT | /mechanics/<id> |
| DELETE | /mechanics/<id> |
| GET | /mechanics/most-tickets |

---

### Service Tickets

| Method | Endpoint |
|---------|----------|
| POST | /service-tickets |
| GET | /service-tickets |
| GET | /service-tickets/<id> |
| PUT | /service-tickets/<id> |
| DELETE | /service-tickets/<id> |
| PUT | /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id> |
| PUT | /service-tickets/<ticket_id>/edit |
| PUT | /service-tickets/<ticket_id>/add-part/<inventory_id> |

---

### Inventory

| Method | Endpoint |
|---------|----------|
| POST | /inventory |
| GET | /inventory |
| GET | /inventory/<id> |
| PUT | /inventory/<id> |
| DELETE | /inventory/<id> |

---

## Authentication

Protected routes require a JWT Bearer Token.

Example Header:

```
Authorization: Bearer YOUR_JWT_TOKEN
```

Login endpoint:

```
POST /customers/login
```

Returns:

```json
{
    "token": "YOUR_JWT_TOKEN"
}
```

---

## Testing

All API endpoints were tested using **Postman**.

The exported Postman collection is included with this project.

---

## Future Improvements

- Password hashing with bcrypt
- Role-based authentication
- Mechanic login
- Inventory quantity tracking
- Search and filtering
- API documentation with Swagger/OpenAPI
- Automated unit testing
- Docker containerization

---
