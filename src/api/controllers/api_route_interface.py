from abc import ABC, abstractmethod

from flask import Flask


class ApiRoute(ABC):
    
    @abstractmethod
    def register(self, server: Flask):
        pass