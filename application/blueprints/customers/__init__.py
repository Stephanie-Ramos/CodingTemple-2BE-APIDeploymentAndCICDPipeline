# A blueprint is used to organize related routes into a separate section of your application. In this case, the blueprint will hold all customer-related routes
from flask import Blueprint

customers_bp = Blueprint(
    # Blueprint name
    "customers",
    # Built-in Python variable. It tells Flask where this blueprint is located so Flask can find related resources, such as templates and static files
    __name__
)

# Import application factory so Flask can register it
# The routes import must come after the blueprint is initialized. Otherwise, it can create a circular import error
# If the routes were imported before customers_bp was created, Python would try to import an object that does not exist yet
from application.blueprints.customers import routes