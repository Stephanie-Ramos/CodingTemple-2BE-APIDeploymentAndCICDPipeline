# Imports the create_app function from the application package in application/__init__.py
from application import create_app

from config import ProductionConfig

# Create this application using my production settings 
app = create_app(ProductionConfig)