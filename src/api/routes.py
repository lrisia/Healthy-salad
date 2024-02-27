from abc import ABC, abstractmethod
from flask_openapi3 import APIBlueprint


class ApiRouteInterface(ABC):

    @abstractmethod
    def register(self, app: APIBlueprint):
        pass


class RouteList:
    __routes: list[ApiRouteInterface] = []

    def add(self, route: ApiRouteInterface):
        self.__routes.append(route)

    def register_to_blueprint(self, blueprint: APIBlueprint) -> APIBlueprint:
        for route in self.__routes:
            route.register(blueprint)
        return blueprint
