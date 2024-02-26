from pydantic import BaseModel

class LineUser(BaseModel):
    userId: str
    