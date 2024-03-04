from pydantic import BaseModel
import requests


class GCPAuthToken(BaseModel):
    access_token: str
    expires_in: int
    token_type: str
  
class CredentialManager():
    __gcp_auth_token: GCPAuthToken
  
    def get_gcp_auth_token(self) -> GCPAuthToken:
        return self.__gcp_auth_token
    
    def refresh(self):
        url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
        headers = {"Metadata-Flavor": "Google"}
        response = requests.get(url, headers=headers).json()
        self.__gcp_auth_token = GCPAuthToken(**response)