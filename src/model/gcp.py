from typing import Union
from google.oauth2.credentials import Credentials
from pydantic import BaseModel
import requests
from google.cloud import aiplatform


class GCPAuthToken(BaseModel):
    access_token: str
    expires_in: int
    token_type: str


class GCPVertexAI:
    __custom_access_token: Union[str, None]
    __gcp_auth_token: GCPAuthToken
    __credential: Credentials

    __project_number: str
    __endpoint_id: str

    __class_names = [
        """สันนิษฐานว่าเป็นโรคใบไหม้ มีลักษณะของขอบใบเริ่มเป็นสีน้ำตาลไหม้ 
สาเหตุเกิดจากผักคายน้ำในขณะที่อากาศร้อนอบอ้าว ทำให้มีความชื้นที่ขอบใบและแดดร้อนทำให้ขอบใบไหม้ 
วิธีแก้ไข ลดอุณหภูมิภายในแปลง โดยการสเปรย์น้ำหรือทำให้อากาศปลอดโปร่ง หลังจากนั้นโรคจะหยุดแพร่กระจาย""",
        """สันนิษฐานว่าเป็นโรคใบจุด มีลักษณะเป็นจุดสีน้ำตาลฉ่ำน้ำ แผลจะขยายเป็นลักษณะวงกลมซ้อนกันเป็นชั้น หากมีอาการรุนแรงใบจะเป็นสีน้ำตาลทั้งแผ่น
สาเหตุเกิดจากเชื้อรา Cercospora sp. (เซอ-โค-สปอร่า) ซึ่งเชื้อรานี้มักจะเจริญเติบโตได้ดีในสภาพแวดล้อมที่ร้อนและความชื้นในอากาศสูง มักจะเกิดในช่วงหน้าฝน
วิธีแก้ไขเบื้องต้นก่อนเป็นโรค จัดแปลงปลูกให้มีการระบายน้ำและอากาศที่ดี หลังจากนั้นโรคจะหยุดแพร่กระจาย""",
        """สันนิษฐานว่ามีสุขภาพดี หากคิดว่าใบสลัดมีปัญหาหรือโรคกรุณาถ่ายภาพในมุมอื่น""",
        """ไม่ทราบปัญหาที่เกิดขึ้น อาจเป็นปัญหาที่ไม่ได้มีต้นเหตุจากใบ หรืออาจะเกิดจากการทำนายที่ผิดพลาด กรุณาลองถ่ายภาพในมุมอื่น""",
        """สันนิษฐานว่าปัญหาเกิดจากหนอน ลักษณะคือมีมูลและร่องรอยการถูกกัดกินบนใบ
วิธีป้องกันสามารถทำได้โดยการหลีกเลี่ยงการปลูกไม้ดอกใกล้แปลง หรือจับผีเสื้อออกหากปลูกภายในโรงเรือน สามารถใช้สารชีวภัณฑ์หรือเคมีที่กำจัดหนอนได้หากต้องการ""",
    ]

    def __init__(
        self,
        custom_access_token: Union[str, None] = None,
        project_number: Union[str, None] = None,
        endpoint_id: Union[str, None] = None,
    ) -> None:
        self.__custom_access_token = custom_access_token
        self.__project_number = project_number or ""
        self.__endpoint_id = endpoint_id or ""

    def init_aiplatform(self) -> None:
        try:
            aiplatform.init(location="asia-southeast1", credentials=self.__credential)
        except:
            self.refresh()
            aiplatform.init(location="asia-southeast1", credentials=self.__credential)

    def refresh(self) -> None:
        if self.__custom_access_token is not None:
            self.__credential = Credentials(self.__custom_access_token)
            return
        url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
        headers = {"Metadata-Flavor": "Google"}
        response = requests.get(url, headers=headers).json()
        self.__gcp_auth_token = GCPAuthToken(**response)
        self.__credential = Credentials(self.__gcp_auth_token.access_token)

    def AuthToken(self) -> GCPAuthToken:
        return self.__gcp_auth_token

    def predict(
        self,
        data: list,
        project_number: Union[str, None] = None,
        endpoint_id: Union[str, None] = None,
    ):
        if project_number is None:
            project_number = self.__project_number
        if endpoint_id is None:
            endpoint_id = self.__endpoint_id
        endpoint = aiplatform.Endpoint(
            endpoint_name=f"projects/{project_number}/locations/asia-southeast1/endpoints/{endpoint_id}"
        )
        result = endpoint.predict(instances=[data])
        return self.__class_names[
            result.predictions[0].index(max(result.predictions[0]))
        ]
