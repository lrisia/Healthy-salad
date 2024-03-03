from flask import Flask
import requests
from api.controllers.gcp.schema import GetGCPAuthTokenResponse
from api.routes import ApiRouteInterface
from flask_openapi3 import APIBlueprint


class GetAuthTokenRoute(ApiRouteInterface):
    def register(self, app: APIBlueprint):
        @app.get("/auth/token", responses={200: GetGCPAuthTokenResponse})
        def get_gcp_auth_token():
            url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
            headers = {"Metadata-Flavor": "Google"}
            response = requests.get(url, headers=headers)
            return response.json()
