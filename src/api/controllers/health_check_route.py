from http import HTTPStatus
from flask import make_response

from api.routes import ApiRouteInterface
from api.shema import ApiTag, DefaultResponse, ErrorResponse


class HealthCheckRoute(ApiRouteInterface):
    def register(self, app):
        @app.get(
            "/healthcheck",
            tags=[ApiTag.Util],
            description="Health check",
            responses={
                200: DefaultResponse,
            },
        )
        def healthcheck():
            return make_response(
                DefaultResponse(message="Healthy").model_dump(), HTTPStatus.OK
            )
