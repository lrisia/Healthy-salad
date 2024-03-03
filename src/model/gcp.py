from pydantic import BaseModel


class GCPAuthToken(BaseModel):
    access_token: str
    expires_in: int
    token_type: str
  