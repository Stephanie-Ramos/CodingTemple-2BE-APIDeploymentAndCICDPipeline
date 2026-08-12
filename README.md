# Mechanic Shop API — Deployment and CI/CD Pipeline

## Project Overview

This project is the final continuation of the **Mechanic Shop API** developed throughout the Backend Software Development module at Coding Temple.

The previous **2 BE Documentation and Testing** project focused on documenting the API with Swagger/OpenAPI and creating automated unit tests for the application's routes.

This project extends that API by preparing it for a **production environment**, deploying it to **Render**, connecting it to a hosted **PostgreSQL database**, and implementing a **CI/CD pipeline with GitHub Actions**.

The completed application demonstrates the transition from a locally developed and tested Flask API to a publicly deployed API with automated testing and deployment.

---

## Previous Assigment vs. Current Project

### Previous Assignment — Documentation and Testing

The previous 2 BE assignment focused primarily on API quality, documentation, and testing.

Features implemented included:

* Swagger/OpenAPI documentation
* Swagger UI
* Route documentation for customers, mechanics, service tickets, and inventory
* Positive and negative unit tests
* Python `unittest`
* Customer authentication testing
* JWT-protected route testing
* CRUD route testing
* Error handling and HTTP status-code validation
* Flask application factory architecture

The goal was to ensure that the API was well documented and that its functionality could be automatically verified before deployment.

### Current Project — Deployment and CI/CD

This project builds on the previous API and adds production deployment and automation.

New features include:

* PostgreSQL database hosted on Render
* Production-specific Flask configuration
* Environment-variable management
* Gunicorn production WSGI server
* Flask API deployed as a Render Web Service
* Production Swagger configuration using HTTPS
* GitHub Actions workflow
* Automated build process
* Automated unit testing
* Automated Render deployment
* GitHub repository secrets
* CI/CD pipeline that prevents deployment when tests fail

The resulting workflow is:

```text
Developer pushes code to GitHub
            ↓
      GitHub Actions
            ↓
          Build
            ↓
           Test
            ↓
    Tests must succeed
            ↓
          Deploy
            ↓
     Render Web Service
            ↓
     PostgreSQL Database
```

---

## Project Progression

This project represents the final stage of the Mechanic Shop API developed throughout the Backend Software Development module.

```text
Mechanic Shop API
        ↓
CRUD + Database Relationships
        ↓
Authentication + Advanced API Features
        ↓
Swagger Documentation
        ↓
Automated Unit Testing
        ↓
Production Configuration
        ↓
PostgreSQL Deployment
        ↓
GitHub Actions
        ↓
Continuous Integration
        ↓
Continuous Deployment
        ↓
Live Production API
```

Compared with the previous **Documentation and Testing** assignment, this final project demonstrates not only that the API works and is documented, but also that it can be **built, tested, and deployed automatically through a production CI/CD workflow**.

---

## Technologies Used

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* SQLAlchemy
* Flask-Marshmallow
* Marshmallow
* Flask-Caching
* Flask-Limiter
* Python-JOSE

### Database

* PostgreSQL — production
* SQLite — automated testing
* SQLAlchemy ORM

### API Documentation

* Swagger / OpenAPI 2.0
* Flask-Swagger
* Flask-Swagger-UI

### Testing

* Python `unittest`
* Flask test client

### Deployment and DevOps

* Render
* Gunicorn
* GitHub
* GitHub Actions
* GitHub Actions Secrets

---

## API Features

The Mechanic Shop API manages the primary operations of a mechanic shop.

The API includes functionality for:

### Customers

* Create customers
* Retrieve customers
* Retrieve individual customers
* Update customers
* Delete customers
* Customer login
* JWT authentication
* Retrieve authenticated customer's service tickets

### Mechanics

* Create mechanics
* Retrieve mechanics
* Retrieve individual mechanics
* Update mechanics
* Delete mechanics

### Service Tickets

* Create service tickets
* Retrieve service tickets
* Retrieve individual service tickets
* Update service tickets
* Delete service tickets
* Associate customers with service tickets
* Associate mechanics with service tickets

### Inventory

The API also supports inventory-related functionality associated with mechanic shop operations.

---

## Project Structure

```text
project/
│
├── .github/
│   └── workflows/
│       └── main.yaml
│
├── application/
│   ├── blueprints/
│   │   ├── customers/
│   │   ├── mechanics/
│   │   └── service_tickets/
│   │
│   ├── utils/
│   │   └── auth.py
│   │
│   └── __init__.py
│
├── tests/
│   ├── test_customers.py
│   ├── test_mechanics.py
│   └── ...
│
├── .env
├── .gitignore
├── config.py
├── flask_app.py
├── requirements.txt
└── README.md
```

The `.env` file is excluded from GitHub using `.gitignore` and should never be committed to the repository.

---

## Production Configuration

The previous version of the application was primarily configured for local development.

This project introduces a separate `ProductionConfig` for the deployed application.

Sensitive values are retrieved through environment variables using Python's `os` package.

Examples include:

```text
DATABASE_URL
SECRET_KEY
```

The production configuration allows the application to use different settings without hard-coding database credentials or secret keys into the source code.

---

## Environment Variables

Sensitive configuration values are not stored directly in the repository.

The application uses environment variables for values such as:

```text
DATABASE_URL
SECRET_KEY
```

For local development, sensitive values can be stored in a `.env` file.

The `.env` file is included in `.gitignore` so credentials are not committed to GitHub.

Render environment variables are configured separately through the Render Web Service.

GitHub Actions secrets are configured through the GitHub repository settings.

---

## Database

The production application uses a **PostgreSQL database hosted on Render**.

During local development, the Render External Database URL can be used when a connection to the hosted PostgreSQL database is required.

The deployed Flask Web Service uses Render's **Internal Database URL** to communicate with the PostgreSQL database within Render.

SQLAlchemy provides the ORM layer between Flask and PostgreSQL.

---

## Gunicorn

The previous assignment used Flask's development server when running locally.

For production deployment, this project uses **Gunicorn** as the WSGI server.

The production application is exposed through:

```python
app = create_app(ProductionConfig)
```

inside:

```text
flask_app.py
```

Render starts the application using:

```bash
gunicorn flask_app:app
```

The previous `app.run()` development-server command is therefore not required for production.

---

## Installation

Clone the repository:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

Navigate into the project:

```bash
cd CodingTemple-2BE-APIDeploymentAndCICDPipeline
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment on macOS/Linux:

```bash
source venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

---

## Running Tests

The project uses Python's built-in `unittest` framework.

Run the complete test suite with:

```bash
python -m unittest discover -s tests
```

The test suite verifies the behavior of the API before changes are allowed to proceed through the deployment stage of the CI/CD pipeline.

---

## Swagger API Documentation

Swagger documentation from the previous Documentation and Testing assignment remains part of the deployed API.

For production, Swagger was updated to use the Render hostname and HTTPS:

```python
swag["host"] = "mechanic-shop-api-08qs.onrender.com"
swag["basePath"] = "/"
swag["schemes"] = ["https"]
```

### Live Swagger Documentation

https://mechanic-shop-api-08qs.onrender.com/api/docs/

Swagger can be used to review the available endpoints, request parameters, authentication requirements, response structures, and HTTP status codes.

---

## Render Deployment

The Flask API is deployed as a **Render Web Service**.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn flask_app:app
```

### Production Environment Variables

Render stores the application's sensitive production configuration, including:

```text
DATABASE_URL
SECRET_KEY
```

These values are not stored directly in the GitHub repository.

### Live API

https://mechanic-shop-api-08qs.onrender.com

---

## CI/CD Pipeline

A major addition in this project is the implementation of a **Continuous Integration and Continuous Deployment (CI/CD) pipeline** using GitHub Actions.

The workflow configuration is located at:

```text
.github/workflows/main.yaml
```

The workflow automatically runs when changes are pushed to the configured branch.

### Build Job

The build job:

1. Checks out the GitHub repository.
2. Sets up Python.
3. Upgrades `pip`.
4. Installs the dependencies from `requirements.txt`.

### Test Job

The test job runs after the build job.

It executes:

```bash
python -m unittest discover -s tests
```

The application must successfully pass its automated tests before deployment can continue.

### Deploy Job

The deploy job depends on the test job:

```yaml
needs: test
```

This means deployment only occurs after the test suite succeeds.

After successful testing, GitHub Actions uses the Render API to trigger a new deployment of the Flask Web Service.

---

## GitHub Actions Secrets

Sensitive information used by the workflow is stored through **GitHub Actions repository secrets** rather than directly inside `main.yaml`.

The workflow uses secrets including:

```text
SECRET_KEY
DATABASE_URL
RENDER_API_KEY
SERVICE_ID
```

This keeps credentials and deployment information separate from the source code.

---

## CI/CD Workflow

The completed CI/CD process follows this sequence:

```text
git push
    ↓
GitHub Repository
    ↓
GitHub Actions
    ↓
Build
    ↓
Test
    ↓
Deploy
    ↓
Render
    ↓
Flask API
    ↓
PostgreSQL
```

If the automated tests fail, the deployment job does not execute.

If the tests pass, GitHub Actions triggers the Render deployment automatically.

This provides a safer and more consistent deployment process than manually redeploying the application after every code change.

---

## Security

Several practices are used to prevent sensitive information from being exposed:

* `.env` is excluded through `.gitignore`.
* Database credentials are not hard-coded into the application.
* Secret keys are stored as environment variables.
* GitHub Actions uses repository secrets.
* Render stores production environment variables separately from the source code.
* JWT authentication protects applicable customer routes.

Sensitive credentials should never be committed to GitHub.

---

## Live Application

### Render API

https://mechanic-shop-api-08qs.onrender.com

### Swagger Documentation

https://mechanic-shop-api-08qs.onrender.com/api/docs/

### GitHub Repository

Add the GitHub repository URL here:

```text
https://github.com/Stephanie-Ramos/CodingTemple-2BE-APIDeploymentAndCICDPipeline
```

---