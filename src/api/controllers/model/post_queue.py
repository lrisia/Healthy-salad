# from flask import Flask
# from api.api_route_interface import ApiRouteInterface


# class ModelPostRoute(ApiRouteInterface):
#     def register(self, server: Flask):
#         @server.route('/model/predict', methods=['GET'])
#         def model_post():
#             return "This should be POST for send image", 200