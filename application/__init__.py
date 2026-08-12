# The Flask class is used to create your web application
from flask import Flask, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

# Import extension objects
from application.extensions import cache, db, limiter, ma
# Import configuration: imports Config class from config.py.
from config import Config

# Create the Application Factory
def create_app(config_class=Config):
    # Create the Flask application: creates the Flask application object
    app = Flask(__name__)

    # Load configuration: Loads all settings from your Config class
    app.config.from_object(config_class)

    # Initialize SQLAlchemy
    # Use this Flask application. SQLAlchemy can: connect to MySQL, create tables, query data, save data
    db.init_app(app)
    # Initialize Marshmallow
    # This line connects Marshmallow to your Flask application. Now schemas can serialize and deserialize data
    ma.init_app(app)
    # This initializes your Flask-Caching extension with your Flask application
    # Once initialized, Flask-Caching can read the settings you placed in config.py
    # Then you're able to use your cache decorator in a route
    cache.init_app(app)
    # Same but for Flask-Limiter
    # Once initialized, able to use on your routes
    limiter.init_app(app)
    
    # Import Blueprints
    # Avoids circular imports
    from application.blueprints.customers import customers_bp
    from application.blueprints.mechanics import mechanics_bp
    from application.blueprints.service_tickets import service_tickets_bp
    from application.blueprints.inventory import inventory_bp


    # Register application blueprints
    app.register_blueprint(
        # This is the blueprint being registered 
        # It contains routes like: @customers_bp.route("/")
        customers_bp,
        url_prefix="/customers"
    )
    
    app.register_blueprint(
        mechanics_bp,
        url_prefix="/mechanics",
    )
    
    app.register_blueprint(
        service_tickets_bp,
        url_prefix="/service-tickets",
    )
    
    app.register_blueprint(
        inventory_bp,
        url_prefix="/inventory"
)
    
    
    # Swagger JSON specification
    @app.route("/swagger")
    def swagger_spec():
        swag = swagger(app)
        
        swag["swagger"] = "2.0"

        swag["info"] = {
            "title": "Mechanic Shop API",
            "description": (
                "API documentation for customers, mechanics, "
                "service tickets, and inventory."
            ),
            "version": "1.0"
        }
        
        # Production Render URL
        swag["host"] = "mechanic-shop-api-08qs.onrender.com"
        swag["basePath"] = "/"
        swag["schemes"] = ["https"]
        
        swag["securityDefinitions"] = {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter: Bearer <your JWT token>"
            }
        }

        return jsonify(swag)

    # Swagger UI
    SWAGGER_URL = "/api/docs"
    API_URL = "/swagger"

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            "app_name": "Mechanic Shop API"
        }
    )

    app.register_blueprint(
        swagger_ui_blueprint,
        url_prefix=SWAGGER_URL
    )

    # Application Context: creates database tables 
    # Use this application while running the following code
    with app.app_context():
        # Importing the models causes Python to load every SQLAlchemy model 
        from application import models
        # Creates every database table that doesn't already exist 
        # Note!: creates missing tables, but it does not modify the structure of an already-existing table. Your Python model changed, but your MySQL table stayed the same
        db.create_all()

    # Returns the completed Flask application 
    return app