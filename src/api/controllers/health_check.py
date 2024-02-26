from flask import Flask
from api.controllers.api_route_interface import ApiRoute


class HealthCheckRoute(ApiRoute):
    def register(self, server: Flask):
        @server.route('/healthcheck', methods=['GET'])
        def health_check():
            return 'eieiei', 200
          
          