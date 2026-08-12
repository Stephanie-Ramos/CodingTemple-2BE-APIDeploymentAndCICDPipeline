# The os module allows your program to interact with the operating system
# One of its most common uses is reading environment variables 
import os


# This class stores all of your Flask configuration settings in one place 
class Config:
    # This tells Flask where your database is located
    # Look for an environment variable with this name 
    SQLALCHEMY_DATABASE_URI = os.getenv(
        
        # Specifies the name of the environment variable 
        "SQLALCHEMY_DATABASE_URI"
    )

    # Turns off SQLAlchemy's event tracking system 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # This retrieves your application's secret key from an environment variable

    SECRET_KEY = os.getenv("SECRET_KEY")
    
    # This tells Flask-Caching what type of cache your application should use
    # SimpleCache: stores cached information temporarily in your application's memory
    CACHE_TYPE = "SimpleCache"
    
    # This establishes the default amount of time cached data remains valid
    # The value is measured in seconds
    # After 60 seconds, the cached value expires, and the next request causes Flask to query the database again and create a new cached result
    CACHE_DEFAULT_TIMEOUT = 60



class TestingConfig(Config):
    TESTING = True
    
    # Tests wil use a temporary in-memory database
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    
    RATELIMIT_ENABLED = False
    
    

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    CACHE_TYPE = "SimpleCache"
    
# This file serves as the central configuration file for your Flask application
# The Config class keeps important application settings in one location