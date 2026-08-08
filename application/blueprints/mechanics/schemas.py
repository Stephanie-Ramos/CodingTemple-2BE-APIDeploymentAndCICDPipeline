# Imports your Marshmallow extension 
from application.extensions import ma
# Imports the Mechanic SQLAlchemy model
from application.models import Mechanic


# Creates a Marshmallow schema based on your SQLAlchemy model
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    # Provides configuration for the schema 
    class Meta:
        # Generate fields from the Mechanic model
        model = Mechanic
        # Allows incoming JSON to be converted into a Mechanic model object
        load_instance = True
        # Includes foreign-key fields when the model contains them
        # The Mechanic model does not directly contain a foreign-key column, but keeping this setting is fine and matches your customer schema pattern
        include_fk = True


# Creates a schema for one mechanic 
mechanic_schema = MechanicSchema()
# Creates a schema for multiple mechanics 
mechanics_schema = MechanicSchema(many=True)