# Mechanic Shop API — Deployment and CI/CD Pipeline

## Project Overview

This project is the final continuation of the **Mechanic Shop API** developed throughout the Backend Software Development module at Coding Temple.

The previous **2 BE Documentation and Testing** project focused on documenting the API with Swagger/OpenAPI and creating automated unit tests for the application's routes.

This project extends that API by preparing it for a **production environment**, deploying it to **Vercel** as a serverless Flask application, connecting it to a hosted **Neon PostgreSQL database**, and implementing a **CI/CD pipeline with GitHub Actions**.

The completed application demonstrates the transition from a locally developed and tested Flask API to a publicly deployed API with automated building, testing, and deployment.

---

## Previous Assignment vs. Current Project

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

* Neon serverless PostgreSQL database
* Production-specific Flask configuration
* Environment-variable management
* Flask API deployed on Vercel as a serverless function
* Production Swagger configuration using HTTPS
* GitHub Actions workflow
* Automated build verification
* Automated unit testing
* Automated Vercel deployment
* GitHub repository secrets
* CI/CD pipeline that prevents deployment when the build or tests fail

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
 Build and tests must succeed
            ↓
          Deploy
            ↓
     Vercel (Flask API)
            ↓
     Neon PostgreSQL Database
```

---

## Migration Notes: Render to Vercel

The API was originally deployed as a Render Web Service backed by a Render PostgreSQL database. It now runs on Vercel with a Neon database.

| Area | Previously (Render) | Now (Vercel) |
|---|---|---|
| Hosting | Render Web Service | Vercel serverless function |
| Web server | Gunicorn (`gunicorn flask_app:app`) | Managed by Vercel (no Gunicorn needed) |
| Entrypoint | `flask_app:app` start command | `index.py` at the project root imports `app` from `flask_app.py` |
| Database | Render PostgreSQL | Neon PostgreSQL (pooled connection string) |
| DB connections | Standard SQLAlchemy connection pool | `NullPool`, because serverless functions are short-lived |
| Swagger host | Hard-coded Render hostname | Taken from the incoming request (`request.host`) |
| Deploy step | Render API call from GitHub Actions | Vercel CLI from GitHub Actions |
| Workflow secrets | `RENDER_API_KEY`, `SERVICE_ID` | `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` |

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
Neon PostgreSQL Database
        ↓
GitHub Actions
        ↓
Continuous Integration
        ↓
Continuous Deployment to Vercel
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
* python-dotenv
* psycopg2

### Database

* PostgreSQL on Neon — production
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

* Vercel
* Vercel CLI
* Neon
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

### Root Route

`GET /` returns a short JSON message with a link to the Swagger documentation.

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
│   │   ├── service_tickets/
│   │   └── inventory/
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
├── .python-version
├── config.py
├── flask_app.py
├── index.py
├── requirements.txt
└── README.md
```

Key deployment files:

* `index.py` — the Vercel entrypoint. It contains a single line, `from flask_app import app`.
* `.python-version` — pins the Python version used for deployment.
* `flask_app.py` — builds the application with `ProductionConfig`.

The `.env` file is excluded from GitHub using `.gitignore` and should never be committed to the repository. The `.vercel` folder created by the Vercel CLI is also excluded.

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

Because Vercel runs the API as short-lived serverless functions, `ProductionConfig` disables SQLAlchemy's own connection pooling and relies on Neon's connection pooler instead:

```python
from sqlalchemy.pool import NullPool

class ProductionConfig(Config):
    SQLALCHEMY_ENGINE_OPTIONS = {"poolclass": NullPool}
```

---

## Environment Variables

Sensitive configuration values are not stored directly in the repository.

The application uses environment variables for values such as:

```text
DATABASE_URL
SECRET_KEY
```

For local development, sensitive values can be stored in a `.env` file:

```text
DATABASE_URL=<your Neon pooled connection string>
SECRET_KEY=<a long random string>
```

Enter the values without quotation marks. Each line must be in `NAME=value` format.

Vercel environment variables are configured per project, either in the Vercel dashboard under **Settings → Environment Variables** or with the Vercel CLI:

```bash
vercel env add DATABASE_URL
vercel env add SECRET_KEY
```

Both are stored as **Secret** variables for the **Production** environment. GitHub Actions secrets are configured separately through the GitHub repository settings.

---

## Database

The production application uses a **PostgreSQL database hosted on Neon**.

The application connects through Neon's **pooled** connection string (the hostname contains `-pooler`). This is the same connection string used in local development when a connection to the hosted database is required.

SQLAlchemy provides the ORM layer between Flask and PostgreSQL.

The application factory calls `db.create_all()` at startup, so any missing tables are created automatically in the Neon database.

Automated tests do not use Neon. They run against an in-memory SQLite database through `TestingConfig`.

Neon may pause an idle database, so the first request after a quiet period can take a few extra seconds.

---

## Vercel Deployment

The Flask API is deployed on **Vercel**. Vercel detects the Flask application through the `index.py` entrypoint at the project root and runs it as a single serverless function. A separate WSGI server such as Gunicorn is not required.

The production application is created inside `flask_app.py`:

```python
app = create_app(ProductionConfig)
```

and exposed to Vercel through `index.py`:

```python
from flask_app import app
```

### Deploying Manually

Install the Vercel CLI, log in, and deploy to production from the project folder:

```bash
npm install -g vercel
vercel login
vercel --prod
```

### Production Environment Variables

Vercel stores the application's sensitive production configuration, including:

```text
DATABASE_URL
SECRET_KEY
```

These values are not stored directly in the GitHub repository. Environment variable changes apply to new deployments, so redeploy after changing them.

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

Create a `.env` file with `DATABASE_URL` and `SECRET_KEY`, then start the development server:

```bash
flask --app flask_app run
```

The API is available at `http://127.0.0.1:5000` and the Swagger documentation at `http://127.0.0.1:5000/api/docs/`.

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

The OpenAPI specification is generated by Flask-Swagger at `/swagger`, and Swagger UI is served at `/api/docs/`.

For production, the Swagger host is taken from the incoming request, so the documentation always points at the domain that is serving it (production, a preview deployment, or localhost). HTTPS is used for the scheme:

```python
swag["host"] = request.host
swag["basePath"] = "/"
swag["schemes"] = ["https"]
```

### Live Swagger Documentation

https://mechanic-shop-api.vercel.app/api/docs/

Swagger can be used to review the available endpoints, request parameters, authentication requirements, response structures, and HTTP status codes.

---

## CI/CD Pipeline

A major addition in this project is the implementation of a **Continuous Integration and Continuous Deployment (CI/CD) pipeline** using GitHub Actions.

The workflow configuration is located at:

```text
.github/workflows/main.yaml
```

The workflow runs on pushes to `main` and on pull requests targeting `main`.

### Build Job

The build job:

1. Checks out the GitHub repository.
2. Sets up Python 3.12.
3. Upgrades `pip`.
4. Installs the dependencies from `requirements.txt`.
5. Runs `pip check` to confirm the installed dependencies are consistent.
6. Compiles all source files with `python -m compileall`.
7. Runs a smoke test that creates the Flask application with `TestingConfig`, confirming the app can start in a clean environment without connecting to a real database.

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

It also only runs for pushes to the `main` branch, so pull requests are built and tested but never deployed.

After successful testing, GitHub Actions installs the Vercel CLI and deploys the application to production:

```bash
vercel deploy --prod --yes --token=$VERCEL_TOKEN
```

---

## GitHub Actions Secrets

Sensitive information used by the workflow is stored through **GitHub Actions repository secrets** rather than directly inside `main.yaml`.

The workflow uses secrets including:

```text
SECRET_KEY
VERCEL_TOKEN
VERCEL_ORG_ID
VERCEL_PROJECT_ID
```

`VERCEL_ORG_ID` and `VERCEL_PROJECT_ID` come from the `.vercel/project.json` file created when the project is linked with the Vercel CLI. `VERCEL_TOKEN` is a Vercel access token scoped to the team that owns the project.

`DATABASE_URL` is stored in Vercel's environment variables rather than in GitHub, because automated tests run on SQLite.

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
Deploy (main branch only)
    ↓
Vercel
    ↓
Flask API
    ↓
Neon PostgreSQL
```

If the build or the automated tests fail, the deployment job does not execute.

If they pass on a push to `main`, GitHub Actions deploys the new version to Vercel automatically.

This provides a safer and more consistent deployment process than manually redeploying the application after every code change.

---

## Security

Several practices are used to prevent sensitive information from being exposed:

* `.env` and `.vercel` are excluded through `.gitignore`.
* Database credentials are not hard-coded into the application.
* Secret keys are stored as environment variables.
* GitHub Actions uses repository secrets.
* Vercel stores production environment variables separately from the source code, as Secret variables.
* JWT authentication protects applicable customer routes.

Sensitive credentials should never be committed to GitHub.

---

## Deployment Considerations

* **Cold starts:** the first request after a period of inactivity is slower, because the serverless function starts up and the Neon database may need to wake.
* **Rate limiting and caching:** Flask-Limiter and Flask-Caching use in-memory storage, which is separate for each serverless instance. Limits and cached values are therefore not shared across instances.
* **Table creation:** `db.create_all()` creates missing tables but does not modify the structure of existing tables.
* **Redirect on the docs URL:** `/api/docs` redirects to `/api/docs/` (with a trailing slash).

---

## Live Application

### Vercel API

https://mechanic-shop-api.vercel.app

### Swagger Documentation

https://mechanic-shop-api.vercel.app/api/docs/

### GitHub Repository

```text
https://github.com/Stephanie-Ramos/CodingTemple-2BE-APIDeploymentAndCICDPipeline
```