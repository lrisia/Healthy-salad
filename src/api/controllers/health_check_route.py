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
                # 500: ErrorResponse,
            }
        )
        def health_check():
            return make_response({"message": "Healthy"}, HTTPStatus.OK)
