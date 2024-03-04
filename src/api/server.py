import logging
import os
from re import template
import sys
from typing import Union
from flask import Blueprint, request
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from api.controllers.gcp.auth_token_get_route import AuthTokenGetRoute
from api.controllers.health_check_route import HealthCheckRoute
from flask_openapi3 import Info
from flask_openapi3 import OpenAPI, APIBlueprint
from api.controllers.line.line_webhook_post_route import LineWebhookPostRoute
from api.controllers.model.model_get_page_route import ModelGetPageRoute
from api.controllers.model.model_predict_post_route import ModelPredictPostRoute
from api.routes import RouteList
from model.config import get_config

from model.container import _Container


class Server:
    server: OpenAPI
    __routes: RouteList = RouteList()
    __api_prefix: str = "/api/v1"

    def __init__(self, container: _Container):
        self.__container = container
        # * Create server instance
        self.server = OpenAPI(
            __name__,
            info=Info(title="Healthy salad Open API", version="1.0.0"),
            template_folder=os.path.join(container.Config().ROOT_DIR, "templates"),
            static_url_path="/static",
            doc_prefix=f"{self.__api_prefix}/docs",
            swagger_url="/",
        )
        self.server.logger.setLevel(logging.INFO)

        # * Middleware
        self._register_middleware()

        # * Register routes
        self._register_routes()

    def _register_routes(self):
        api_blueprint = APIBlueprint("api-v1", __name__, url_prefix=self.__api_prefix)
        page_blueprint = Blueprint("page", __name__)

        self.__routes.add(HealthCheckRoute())

        # GCP
        self.__routes.add(AuthTokenGetRoute(self.__container.GCPVertexAI()))

        # Line
        self.__routes.add(LineWebhookPostRoute(self.__container.LineConnection()))

        # Model
        self.__routes.add(ModelGetPageRoute())
        self.__routes.add(
            ModelPredictPostRoute(
                self.__container.GCPVertexAI(), self.__container.TaskQueueManager()
            )
        )

        self.server.register_api(self.__routes.register_to_blueprint(api_blueprint))
        self.server.register_blueprint(self.__routes.register_to_app(page_blueprint))

    def _register_middleware(self):
        # self.server.wsgi_app = ProxyFix(self.server.wsgi_app)
        pass

    def start(self, port: int, debug: bool = get_config().DEBUG) -> None:
        self.server.run(host="0.0.0.0", port=port, debug=debug)

    def terminate(self):
        shutdown = request.environ.get("werkzeug.server.shutdown")
        if shutdown is not None:
            shutdown()
