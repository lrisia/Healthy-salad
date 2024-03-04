import os
from dotenv import load_dotenv

from exception.env_except import EnvExcept


class _Config:
    ENVIRONMENT: str
    DEBUG: bool
    SERVER_PORT: int

    LINE_CHANNEL_SECRET: str
    LINE_LINE_CHANNEL_ACCESS_TOKEN: str
    
    GCP_PROJECT_NUMBER: str
    GCP_ENDPOINT_ID: str

    GCP_PROJECT_NUMBER: str
    GCP_ENDPOINT_ID: str
    FIRESTORE_SERVICE_ACCOUNT: str

    ROOT_DIR: str

    def __init__(self):
        load_dotenv()
        self.ENVIRONMENT = self._get_environment()
        self.DEBUG = True if self.ENVIRONMENT == "development" else False
        self.SERVER_PORT = int(os.environ.get("SERVER_PORT", 8080))
        self.LINE_CHANNEL_SECRET = self._required_env("LINE_CHANNEL_SECRET")
        self.LINE_LINE_CHANNEL_ACCESS_TOKEN = self._required_env(
            "LINE_CHANNEL_ACCESS_TOKEN"
        )
        self.GCP_PROJECT_NUMBER = self._required_env("GCP_PROJECT_NUMBER")
        self.GCP_ENDPOINT_ID = self._required_env("GCP_ENDPOINT_ID")
        self.FIRESTORE_SERVICE_ACCOUNT = self._required_env("FIRESTORE_SERVICE_ACCOUNT")
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def _required_env(self, env: str) -> str:
        value = os.environ.get(env)
        if value is None:
            # raise EnvExcept(f"{env} is not set.")
            print(f"{env} is not set.")
            return ""
        return value

    def _get_environment(self) -> str:
        environment = os.environ.get("ENVIRONMENT")
        if environment == "development":
            return environment
        return "production"


config = _Config()


def get_config():
    return config
