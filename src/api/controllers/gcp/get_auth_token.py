from flask import Flask
import requests
from api.routes import ApiRouteInterface
from flask_openapi3 import APIBlueprint


class ModelPostRoute(ApiRouteInterface):
    def register(self, app: APIBlueprint):
        @app.get("/auth/token")
        def callback():
            url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
            headers = {"Metadata-Flavor": "Google"}
            response = requests.get(url, headers=headers)
            return response.json()
