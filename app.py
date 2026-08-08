# Imports the create_app function from the application package in application/__init__.py
from application import create_app

# The function builds and returns a fully configured Flask application 
app = create_app()

# Checks whether this file is being run directly
if __name__ == "__main__":
    # Starts Flask’s development server 
    app.run(debug=True, port=5001)