from flask import make_response
from api.routes import ApiRouteInterface
from api.shema import ApiTag, ErrorResponse, HttpStatus
from model.gcp import GCPAuthToken, GCPVertexAI


class AuthTokenGetRoute(ApiRouteInterface):
    __GCPVertexAI: GCPVertexAI

    def __init__(self, gcp_vertex_ai: GCPVertexAI) -> None:
        self.__GCPVertexAI = gcp_vertex_ai

    def register(self, app):
        @app.get(
            "auth/token",
            tags=[ApiTag.GoogleCloudPlatform],
            description="Get a new auth token. If the token is expired, it will be refreshed.",
            responses={
                HttpStatus.OK: GCPAuthToken,
                HttpStatus.INTERNAL_SERVER_ERROR: ErrorResponse,
            },
        )
        def auth_token_get():
            try:
                self.__GCPVertexAI.refresh()
                return make_response(
                    self.__GCPVertexAI.AuthToken().model_dump(), HttpStatus.OK
                )
            except Exception as e:
                return make_response(
                    ErrorResponse(message="Get auth token from gcp failed. If this run in local, please try to check 'ACCESS_TOKEN' in .env", stacktrace=e.__str__()).model_dump(),
                    HttpStatus.INTERNAL_SERVER_ERROR,
                )
