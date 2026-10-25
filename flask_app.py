from dotenv import load_dotenv

load_dotenv()

from application import create_app
from config import ProductionConfig

app = create_app(ProductionConfig)