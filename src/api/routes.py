from abc import ABC, abstractmethod
from typing import Union
from flask import Blueprint, Flask
from flask_openapi3 import APIBlueprint


class ApiRouteInterface(ABC):

    @abstractmethod
    def register(self, app: APIBlueprint):
        pass


class PageRouteInterface(ABC):

    @abstractmethod
    def register(self, app: Blueprint):
        pass


class RouteList:
    __api_routes: list[ApiRouteInterface] = []
    __page_routes: list[PageRouteInterface] = []

    def add(self, route: Union[ApiRouteInterface, PageRouteInterface]):
        if (isinstance(route, ApiRouteInterface)):
            self.__api_routes.append(route)
        else:
            self.__page_routes.append(route)

    def register_to_blueprint(self, blueprint: APIBlueprint) -> APIBlueprint:
        for route in self.__api_routes:
            route.register(blueprint)
        return blueprint
    
    def register_to_app(self, blueprint: Blueprint) -> Blueprint:
        for route in self.__page_routes:
            route.register(blueprint)
        return blueprint
