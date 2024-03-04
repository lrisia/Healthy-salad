import logging
import os
from re import template
from typing import Union
from flask import Blueprint, request
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from api.controllers.gcp.get_auth_token_route import GetAuthTokenRoute
from api.controllers.health_check_route import HealthCheckRoute
from flask_openapi3 import Info
from flask_openapi3 import OpenAPI, APIBlueprint
from api.controllers.line.line_webhook_route import PostLineWebhookRoute
from api.controllers.model.get_predict_page_route import GetPredictPageRoute
from api.controllers.model.post_predict_route import PostPredictRoute
from api.routes import RouteList

from config import get_config
from model.gcp import GCPVertexAI
from model.task import TaskQueueManager


class Server:
    server: OpenAPI
    __routes: RouteList
    __prefix: str = "/api/v1"
    __queue_manager: Union[None, TaskQueueManager]
    __vertex_ai: Union[None, GCPVertexAI]

    def __init__(
        self,
        vertex_ai: Union[None, GCPVertexAI] = None,
        queue_manager: Union[None, TaskQueueManager] = None,
    ):
        self.__queue_manager = queue_manager
        self.__vertex_ai = vertex_ai

        # * Create server instance
        self.server = OpenAPI(
            __name__,
            info=Info(title="Healthy salad Open API", version="1.0.0"),
            template_folder=os.path.join(get_config().ROOT_DIR, "templates"),
            static_url_path="/static",
            doc_prefix=f"{self.__prefix}/docs",
            swagger_url="/",
        )
        self.server.config["UPLOAD_FOLDER"] = (
            os.path.join(get_config().ROOT_DIR, "upload"),
        )
        self.server.logger.setLevel(logging.INFO)

        # * Middleware
        self._register_middleware()

        # * Register routes
        self._register_routes()

    def _register_routes(self):
        api_blueprint = APIBlueprint("api-v1", __name__, url_prefix=self.__prefix)
        page_blueprint = Blueprint("page", __name__)

        self.__routes = RouteList()
        self.__routes.add(HealthCheckRoute())

        # Line
        self.__routes.add(
            PostLineWebhookRoute(
                get_config().LINE_LINE_CHANNEL_ACCESS_TOKEN,
                get_config().LINE_CHANNEL_SECRET,
            )
        )

        # GCP
        self.__routes.add(GetAuthTokenRoute())
        self.__routes.add(PostPredictRoute(self.__vertex_ai, self.__queue_manager))

        # Page
        self.__routes.add(GetPredictPageRoute())

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
