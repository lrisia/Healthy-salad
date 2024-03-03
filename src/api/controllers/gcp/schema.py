from pydantic import BaseModel


class GetGCPAuthTokenResponse(BaseModel):
    access_token: str
    expires_in: int
    token_type: str
  