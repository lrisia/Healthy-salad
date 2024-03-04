from typing import List
from pydantic import BaseModel

from api.shema import DefaultResponse


class ModelResponse(DefaultResponse, BaseModel):
    answers: List[float]