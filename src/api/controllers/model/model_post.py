from flask import Flask
from api.controllers.api_route_interface import ApiRoute


class ModelPostRoute(ApiRoute):
    def register(self, server: Flask):
        @server.route('/model/predict', methods=['GET'])
        def model_post():
            return "This should be POST for send image", 200