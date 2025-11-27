import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    AEVO_ENV = os.getenv("AEVO_ENV")
    AEVO_TOKEN = os.getenv("AEVO_TOKEN_API")
    
    @property
    def AEVO_URL_GET_IDEAS(self):
        if not self.AEVO_ENV:
            return None
        return f"https://{os.getenv("AEVO_ENV")}.aevoinnovate.net/webapi/api/ApiExterna/v2/GetIdeias"

    @property
    def AEVO_URL_GET_GET_USERS(self):
        if not self.AEVO_ENV:
            return None
        return f"https://{os.getenv("AEVO_ENV")}.aevoinnovate.net/webapi/api/apiExterna/Usuarios"

settings = Settings()