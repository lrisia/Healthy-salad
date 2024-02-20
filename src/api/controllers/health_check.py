from api.controllers.api_route_interface import ApiRoute


class HealthCheckRoute(ApiRoute):
    def register(self, server):
        @server.route('/healthcheck', methods=['GET'])
        def health_check():
            return 'OK', 200
          
          