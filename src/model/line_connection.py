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

    def handle_message(self, message: str) -> str:
        answer = """สวัสดี ดิฉัน Salady Assistant ผู้ช่วยในการปลูกผักสลัดของคุณยินดีให้บริการค่ะ ดิฉันสามารถวิเคราะห์ปํญหาหรือโรคที่ใบผักสลัดเป็นได้ 
โดยให้คุณส่งรูปภาพของใบผักสลัดมาให้ดิฉัน แล้วดิฉันจะประมวลผลพร้อมแนะนำแนวทางการแก้ไขให้คุณค่ะ
"""
        if "ใบไหม้" in message or "ใบเป็นสีน้ำตาล" in message or "ขอบใบไหม้" in message:
            answer = """สันนิษฐานว่าเป็นโรคใบไหม้ มีลักษณะของขอบใบเริ่มเป็นสีน้ำตาลไหม้ 
สาเหตุเกิดจากผักคายน้ำในขณะที่อากาศร้อนอบอ้าว ทำให้มีความชื้นที่ขอบใบและแดดร้อนทำให้ขอบใบไหม้ 
วิธีแก้ไข ลดอุณหภูมิภายในแปลง โดยการสเปรย์น้ำหรือทำให้อากาศปลอดโปร่ง หลังจากนั้นโรคจะหยุดแพร่กระจาย"""
        elif "ใบจุด" in message or "จุดสีน้ำตาล" in message or "จุด" in message:
            answer = """สันนิษฐานว่าเป็นโรคใบจุด มีลักษณะเป็นจุดสีน้ำตาลฉ่ำน้ำ แผลจะขยายเป็นลักษณะวงกลมซ้อนกันเป็นชั้น หากมีอาการรุนแรงใบจะเป็นสีน้ำตาลทั้งแผ่น
สาเหตุเกิดจากเชื้อรา Cercospora sp. (เซอ-โค-สปอร่า) ซึ่งเชื้อรานี้มักจะเจริญเติบโตได้ดีในสภาพแวดล้อมที่ร้อนและความชื้นในอากาศสูง มักจะเกิดในช่วงหน้าฝน
วิธีแก้ไขเบื้องต้นก่อนเป็นโรค จัดแปลงปลูกให้มีการระบายน้ำและอากาศที่ดี หลังจากนั้นโรคจะหยุดแพร่กระจาย"""
        elif "หนอน" in message or "มูลหนอน" in message or "อึหนอน" in message:
            answer = """สันนิษฐานว่าปัญหาเกิดจากหนอน ลักษณะคือมีมูลและร่องรอยการถูกกัดกินบนใบ
วิธีป้องกันสามารถทำได้โดยการหลีกเลี่ยงการปลูกไม้ดอกใกล้แปลง หรือจับผีเสื้อออกหากปลูกภายในโรงเรือน สามารถใช้สารชีวภัณฑ์หรือเคมีที่กำจัดหนอนได้หากต้องการ"""
        return answer
