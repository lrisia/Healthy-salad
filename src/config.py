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
    
    def __init__(self):
        load_dotenv()
        self.ENVIRONMENT = self.__get_environment()
        self.DEBUG = True if self.ENVIRONMENT == "development" else False
        self.SERVER_PORT = int(os.environ.get("SERVER_PORT", 8080))
        
    def __get_environment(self) -> str:
        environment = os.environ.get("ENVIRONMENT")
        if environment is None:
            raise EnvExcept("ENVIRONMENT is not set")
        elif environment not in ["development", "production"]:
            raise EnvExcept("ENVIRONMENT is not valid")
        return environment
        
def get_config():
    return _Config()