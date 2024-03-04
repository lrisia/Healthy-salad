from abc import ABC, abstractmethod

from model.container import _Container


class CommandInterface(ABC):

    @abstractmethod
    def execute(self, container: _Container) -> None:
        pass
