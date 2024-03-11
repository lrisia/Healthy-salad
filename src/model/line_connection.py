from typing import List, Optional
import numpy as np
from pydantic import BaseModel
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
)
import requests


class LineConnection:
    configuration: Configuration
    handler: WebhookHandler

    def __init__(self, access_token: str, channel_secret: str):
        self.configuration: Configuration = Configuration(access_token=access_token)
        self.handler: WebhookHandler = WebhookHandler(channel_secret)

    def get_content(self, message_id: str) -> np.ndarray:
        response = requests.get(
            f"https://api-data.line.me/v2/bot/message/{message_id}/content",
            headers={"Authorization": f"Bearer {self.configuration.access_token}"},
        )
        return np.frombuffer(response.content, np.uint8)
    
    def send_message(self, user_id: str, message: str) -> None:
        requests.post(
            "https://api.line.me/v2/bot/message/push",
            headers={"Authorization": f"Bearer {self.configuration.access_token}"},
            json={"to": user_id, "messages": [{"type": "text", "text": message}]},
        )
