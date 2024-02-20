from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from api.controllers.health_check import HealthCheckRoute
from api.controllers.model.model_post import ModelPostRoute

from config import get_config

class Server:
    def __init__(self):
        self.__server = Flask(__name__)

    def start(self, port: int, debug: bool = get_config().DEBUG) -> Flask:
        # Set prefix
        self.__server.config["APPLICATION_ROOT"] = "/api/v1"
        
        # Register routes
        self._register_routes()
        
        # Middleware
        self._middleware()
        
        self.__server.run(host="0.0.0.0", port=port, debug=debug)
        return self.__server
    
    def get_server(self) -> Flask:
        return self.__server
        
    def terminate(self):
        shutdown = request.environ.get('werkzeug.server.shutdown')
        if shutdown is not None: shutdown()
        
    def _register_routes(self):
        HealthCheckRoute().register(self.__server)
        
        # Model
        ModelPostRoute().register(self.__server)
        
    def _middleware(self):
        self.__server.wsgi_app = ProxyFix(self.__server.wsgi_app)
        self.__server.wsgi_app = DispatcherMiddleware(NotFound(), {"/api/v1": self.__server.wsgi_app})
        