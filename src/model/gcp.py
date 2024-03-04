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
        return result.predictions[0]
