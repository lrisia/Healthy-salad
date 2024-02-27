from pydantic import BaseModel
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
)


class LineConnection():
    configuration: Configuration
    handler: WebhookHandler

    def __init__(self, access_token: str, channel_secret: str):
        self.configuration: Configuration = Configuration(access_token=access_token)
        self.handler: WebhookHandler = WebhookHandler(channel_secret)
