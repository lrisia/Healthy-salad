from re import M
from typing import Any, Optional
from pydantic import BaseModel
from flask_openapi3 import Tag


class HttpStatus:
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


class ApiTag:
    Util = Tag(name="Util", description="Util API")
    GoogleCloudPlatform = Tag(name="GoogleCloudPlatform", description="Google Cloud Platform API")
    Line = Tag(name="Line", description="Line API")
    Model = Tag(name="Model", description="Model API")


class DefaultResponse(BaseModel):
    message: Optional[str]


class ErrorResponse(DefaultResponse, BaseModel):
    stacktrace: Optional[Any]
