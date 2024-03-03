from http import HTTPStatus
from flask import make_response
from flask_openapi3 import APIBlueprint

from api.routes import ApiRouteInterface
from api.shema import ApiTag, DefaultResponse, ErrorResponse


class HealthCheckRoute(ApiRouteInterface):
    def register(self, app: APIBlueprint):
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
