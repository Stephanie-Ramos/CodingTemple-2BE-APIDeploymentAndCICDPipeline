# Mechanic Shop API — Documentation and Testing

## Project Description

This project is a Flask-based REST API for managing a mechanic shop. It builds upon the previous Mechanic Shop backend project by adding API documentation with Swagger and automated endpoint testing using Python's built-in `unittest` library.

The API manages customers, mechanics, service tickets, and inventory. It also supports relationships between these resources, including assigning mechanics and inventory parts to service tickets.

The primary focus of this project is ensuring that the API is well documented, testable, and reliable as it moves closer to a production-ready application.

---

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Marshmallow
- MySQL
- SQLite for testing
- Flask-Swagger
- Flask-Swagger-UI
- Flask-Caching
- Flask-Limiter
- JWT Authentication
- Python `unittest`
- Postman
- Git
- GitHub

---

## Project Structure

```text
project/
│
├── application/
│   ├── blueprints/
│   │   ├── customers/
│   │   ├── mechanics/
│   │   ├── service_tickets/
│   │   └── inventory/
│   │
│   ├── models/
│   ├── extensions.py
│   └── __init__.py
│
├── tests/
│   ├── __init__.py
│   ├── test_customers.py
│   ├── test_mechanics.py
│   ├── test_service_tickets.py
│   └── test_inventory.py
│
├── app.py
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## API Resources

The API is organized into four primary resources.

### Customers

Customer routes provide functionality for:

- Creating customers
- Retrieving all customers
- Retrieving an individual customer
- Updating customer information
- Deleting customers
- Customer login
- JWT authentication
- Retrieving the authenticated customer's service tickets

### Mechanics

Mechanic routes provide functionality for:

- Creating mechanics
- Retrieving all mechanics
- Retrieving an individual mechanic
- Updating mechanic information
- Deleting mechanics
- Ranking mechanics by number of assigned service tickets

### Service Tickets

Service ticket routes provide functionality for:

- Creating service tickets
- Retrieving all service tickets
- Retrieving individual service tickets
- Assigning mechanics to service tickets
- Editing mechanic assignments
- Adding inventory parts to service tickets

Service tickets are associated with customers and can have multiple mechanics and inventory parts assigned to them.

### Inventory

Inventory routes provide full CRUD functionality for mechanic shop parts:

- Creating inventory parts
- Retrieving all inventory
- Retrieving an inventory part by ID
- Updating inventory parts
- Deleting inventory parts

Inventory parts can also be assigned to service tickets.

---

# API Documentation

API documentation is implemented using:

- `flask-swagger`
- `flask-swagger-ui`

Each documented API route includes information such as:

- Endpoint path
- HTTP request method
- Route tag/category
- Summary
- Description
- Request parameters
- Request payload definitions
- Response definitions
- Example request and response data
- HTTP status codes
- Security requirements for authenticated routes

## Swagger UI

Start the Flask application:

```bash
python app.py
```

The application runs locally on port `5001`.

Open the Swagger UI in a browser:

```text
http://127.0.0.1:5001/api/docs/
```

The Swagger interface provides interactive documentation for the API's Customer, Mechanic, Service Ticket, and Inventory endpoints.

---

# Authentication

Some customer routes are protected using JWT authentication.

A customer first logs in using the login endpoint:

```text
POST /customers/login
```

After successful authentication, the API returns a JWT.

Protected endpoints require the token to be sent using the HTTP Authorization header:

```text
Authorization: Bearer <token>
```

For example, the authenticated customer can retrieve their service tickets through:

```text
GET /customers/my-tickets
```

Requests without a valid authentication token return an authorization error.

---

# Testing

Automated testing is implemented using Python's built-in `unittest` library.

A separate test file is provided for each API blueprint:

```text
tests/
├── __init__.py
├── test_customers.py
├── test_mechanics.py
├── test_service_tickets.py
└── test_inventory.py
```

The tests verify successful API requests as well as negative and edge-case behavior.

Examples of tested behavior include:

- Successful resource creation
- Retrieving resources
- Updating resources
- Deleting resources
- Invalid IDs
- Missing request data
- Duplicate email addresses
- Missing customers
- Missing mechanics
- Missing inventory parts
- Duplicate mechanic assignments
- Duplicate inventory part assignments
- Unauthorized requests
- JWT-protected routes
- Empty API resource lists

## Run All Tests

From the project root directory, activate the virtual environment and run:

### macOS / Linux

```bash
source venv/bin/activate
python -m unittest discover tests
```

### Windows

```bash
venv\Scripts\activate
python -m unittest discover tests
```

A successful test run should finish with:

```text
OK
```

Individual blueprint tests can also be run separately.

For example:

```bash
python -m unittest tests.test_customers
```

```bash
python -m unittest tests.test_mechanics
```

```bash
python -m unittest tests.test_service_tickets
```

```bash
python -m unittest tests.test_inventory
```

---

# Test Database

Testing uses a separate testing configuration so automated tests do not modify the production/development MySQL database.

The test suite creates the required database tables for each test and removes test data after execution.

This allows each test to run independently in a controlled environment.

---

# Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

## 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

## 3. Activate the Virtual Environment

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Configure Environment Variables

Create a `.env` file for sensitive configuration values such as database credentials and JWT secrets.

Example:

```text
DATABASE_URL=<your-database-connection>
SECRET_KEY=<your-secret-key>
```

The `.env` file should not be committed to GitHub.

Make sure `.gitignore` contains:

```text
.env
venv/
__pycache__/
*.pyc
```

## 6. Start the Application

```bash
python app.py
```

The API will run at:

```text
http://127.0.0.1:5001
```

Swagger documentation can be viewed at:

```text
http://127.0.0.1:5001/api/docs/
```

---

# HTTP Status Codes

The API uses standard HTTP status codes, including:

| Status Code | Meaning |
|---|---|
| `200` | Request completed successfully |
| `201` | Resource successfully created |
| `400` | Invalid or missing request data |
| `401` | Authentication required or invalid |
| `403` | User is not authorized to perform the action |
| `404` | Requested resource was not found |
| `409` | Resource conflict, such as duplicate data |

---

# API Testing with Postman

The API can also be manually tested using Postman.

A Postman collection is included with the project to help test API endpoints and authentication workflows.

For protected routes:

1. Log in using the customer login endpoint.
2. Copy the returned JWT.
3. Select **Bearer Token** authentication in Postman.
4. Paste the JWT into the token field.
5. Send the protected request.

Postman is useful for manual API verification, while `unittest` provides repeatable automated testing.

---

# Key Project Features

This project demonstrates:

- RESTful API development with Flask
- Application factory architecture
- Flask Blueprints
- SQLAlchemy ORM
- MySQL database integration
- Marshmallow serialization and validation
- One-to-many relationships
- Many-to-many relationships
- JWT authentication
- Protected API routes
- Rate limiting
- Response caching
- Swagger/OpenAPI documentation
- Automated API testing
- Positive and negative test cases
- HTTP error handling
- Postman API testing

---

# Assignment Objective

The objective of this project is to improve the reliability and maintainability of an existing backend API by incorporating comprehensive documentation and automated testing.

Swagger provides developers with an interactive interface for understanding and testing API endpoints, while Python's `unittest` framework verifies that API resources behave correctly under both successful and unsuccessful conditions.

Together, these additions help prepare the Mechanic Shop API for a more production-ready development workflow.