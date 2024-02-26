import os
from dotenv import load_dotenv

from exception.env_except import EnvExcept


class _Config:
    """Config load from .env

    Attributes:
        ENVIRONMENT: str
        DEBUG: bool
        
        SERVER_PORT: int
    """
    ENVIRONMENT: str
    DEBUG: bool
    SERVER_PORT: int
    
    LINE_CHANNEL_SECRET: str
    LINE_LINE_CHANNEL_ACCESS_TOKEN: str
    
    def __init__(self):
        load_dotenv()
        self.ENVIRONMENT = self.__get_environment()
        self.DEBUG = True if self.ENVIRONMENT == "development" else False
        self.SERVER_PORT = int(os.environ.get("SERVER_PORT", 8080))
        self.LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET") or ""
        self.LINE_LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN") or ""
        
    def __get_environment(self) -> str:
        environment = os.environ.get("ENVIRONMENT")
        if environment == "development":
            return environment
        return "production"
        
def get_config(): 
    return _Config()
