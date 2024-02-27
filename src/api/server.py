import logging
from flask import request
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from api.controllers.health_check_route import HealthCheckRoute
from flask_openapi3 import Info
from flask_openapi3 import OpenAPI, APIBlueprint
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
)
from api.controllers.line.line_webhook import LineWebhookPostRoute
from api.routes import RouteList

from config import get_config


class Server:
    server: OpenAPI
    __routes: RouteList
    __prefix: str = "/api/v1"

    def __init__(self):
        # * Create server instance
        self.server = OpenAPI(
            __name__,
            info=Info(title="Healthy salad Open API", version="1.0.0"),
            doc_prefix=f"{self.__prefix}/docs",
            swagger_url="/",
        )
        self.server.logger.setLevel(logging.INFO)

        # * Middleware
        self._register_middleware()

        # * Register routes
        self._register_routes()

    def _register_routes(self):
        api_blueprint = APIBlueprint("api-v1", __name__, url_prefix=self.__prefix)

        self.__routes = RouteList()
        self.__routes.add(HealthCheckRoute())
        self.__routes.add(
            LineWebhookPostRoute(
                get_config().LINE_LINE_CHANNEL_ACCESS_TOKEN,
                get_config().LINE_CHANNEL_SECRET,
            )
        )

        self.server.register_api(self.__routes.register_to_blueprint(api_blueprint))

    def _register_middleware(self):
        # self.server.wsgi_app = ProxyFix(self.server.wsgi_app)
        pass

    def start(self, port: int, debug: bool = get_config().DEBUG) -> None:
        self.server.run(host="0.0.0.0", port=port, debug=debug)

    def terminate(self):
        shutdown = request.environ.get("werkzeug.server.shutdown")
        if shutdown is not None:
            shutdown()
