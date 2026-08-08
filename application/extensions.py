from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from sqlalchemy.orm import DeclarativeBase

from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create a base class for our models
# Your Base class inherits from SQLAlchemy's DeclarativeBase, 
# which means it receives SQLAlchemy's model and table-mapping behavior
class Base(DeclarativeBase):
    pass


#Instantiate your SQLAlchemy database
# db: Creates the main SQLAlchemy extension object
# ma: Creates a Marshmallow extension object
db = SQLAlchemy(model_class = Base)
ma = Marshmallow()

# Once connected, it is used in the routes
# That tells Flask-Caching to temporarily save the result of that route
cache = Cache()


# This creates the object responsible for rate limiting 
# Allow this client to access this route only 5 times per minute
limiter = Limiter(
    # This tells Flask-Limiter how to identify clients when counting requests
    # get_remote_address: retrieves the client's IP address
    key_func=get_remote_address,
    # it stores those counters in the application's memory
    storage_uri="memory://"
)

# This file serves as a central location for creating and configuring the Flask extensions 
# used throughout your Mechanic Shop API. In this project, it creates extension objects for 
# features such as SQLAlchemy, Marshmallow, Flask-Caching, and Flask-Limiter