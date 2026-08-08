from flask import Blueprint


inventory_bp = Blueprint(
    "inventory",
    __name__
)


# Import routes after creating the blueprint
# to avoid circular import errors
from application.blueprints.inventory import routes