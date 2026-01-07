import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL")
    API_TOKEN = os.getenv("API_TOKEN")

    @staticmethod
    def validate():
        if not Config.BASE_URL or not Config.API_TOKEN:
            raise ValueError("Missing API_BASE_URL or API_TOKEN in .env file")

# Validate immediately upon import
Config.validate()