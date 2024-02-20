from flask import Flask
from api.controllers.api_route_interface import ApiRoute


class ModelPostRoute(ApiRoute):
    def register(self, server: Flask):
        @server.route('/route', methods=['POST'])
        def model_post():
            return "ok", 200