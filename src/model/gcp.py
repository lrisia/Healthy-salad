from google.oauth2.credentials import Credentials
from pydantic import BaseModel
import requests


class GCPAuthToken(BaseModel):
    access_token: str
    expires_in: int
    token_type: str


class CredentialManager:
    __gcp_auth_token: GCPAuthToken
    __credential: Credentials

    def get_credential(self) -> Credentials:
        return self.__credential

    def refresh(self):
        url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
        headers = {"Metadata-Flavor": "Google"}
        response = requests.get(url, headers=headers).json()
        self.__gcp_auth_token = GCPAuthToken(**response)
        self.__credential = Credentials(self.__gcp_auth_token.access_token)
