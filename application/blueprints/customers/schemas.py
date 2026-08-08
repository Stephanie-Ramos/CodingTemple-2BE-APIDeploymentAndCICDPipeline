# Imports the Marshmallow extension object named ma
# ma: helps to create schemas that convert SQLAlchemy objects to JSON and incoming JSON into Python data or model instances
from application.extensions import ma
# models will now live inside application/models.py
from application.models import Customer


# Creates a schema class named CustomerSchema
# Automatically creates Marshmallow fields based on the columns in your Customer model
class CustomerSchema(ma.SQLAlchemyAutoSchema):

    # Creates an inner configuration class named Meta
    # Meta contains instructions that tell Marshmallow how to build and use the schema
    class Meta:
        # This schema is based on the Customer SQLAlchemy model
        model = Customer
        # Create a Customer model object when JSON is deserialized
        load_instance = True
        # Include foreign-key fields in the automatically generated schema
        include_fk = True


# Creates one instance of CustomerSchema
customer_schema = CustomerSchema()
# # Creates many instances of CustomerSchema
customers_schema = CustomerSchema(many=True)

# For login, only validate the email and password fields 
login_schema = CustomerSchema(
    only=("email", "password")
)