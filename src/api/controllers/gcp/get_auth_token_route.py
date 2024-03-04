import requests
from api.routes import ApiRouteInterface


class GetAuthTokenRoute(ApiRouteInterface):
    def register(self, app):
        @app.get("auth/token")
        def get_auth_token():
            url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
            headers = {"Metadata-Flavor": "Google"}
            response = requests.get(url, headers=headers)
            return response.json()