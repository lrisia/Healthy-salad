import os
from dotenv import load_dotenv

from exception.env_except import EnvExcept


class _Config:
    ENVIRONMENT: str
    DEBUG: bool
    SERVER_PORT: int

    LINE_CHANNEL_SECRET: str
    LINE_LINE_CHANNEL_ACCESS_TOKEN: str

    def __init__(self):
        load_dotenv()
        self.ENVIRONMENT = self._get_environment()
        self.DEBUG = True if self.ENVIRONMENT == "development" else False
        self.SERVER_PORT = int(os.environ.get("SERVER_PORT", 8080))
        self.LINE_CHANNEL_SECRET = self._required_env("LINE_CHANNEL_SECRET")
        self.LINE_LINE_CHANNEL_ACCESS_TOKEN = self._required_env(
            "LINE_CHANNEL_ACCESS_TOKEN"
        )

    def _required_env(self, env: str) -> str:
        value = os.environ.get(env)
        if value is None:
            # raise EnvExcept(f"{env} is not set.")
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
