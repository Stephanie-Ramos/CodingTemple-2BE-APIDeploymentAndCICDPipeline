# The os module allows your program to interact with the operating system
# One of its most common uses is reading environment variables 
import os 
from sqlalchemy.pool import NullPool;


class Config:
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL")
        or os.getenv("SQLALCHEMY_DATABASE_URI")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY")

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    RATELIMIT_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_ENGINE_OPTIONS = {"poolclass": NullPool}
    
# This file serves as the central configuration file for your Flask application
# The Config class keeps important application settings in one location