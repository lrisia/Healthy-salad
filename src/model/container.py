from model.gcp import GCPVertexAI
from model.line_connection import LineConnection
from model.task import TaskQueueManager
from model.config import _Config, get_config


class _Container:
    __Config: _Config
    __GCPVertexAI: GCPVertexAI
    __TaskQueueManager: TaskQueueManager
    __LineConnection: LineConnection

    def __init__(self) -> None:
        self.__Config = get_config()
        self.__GCPVertexAI = GCPVertexAI(
            self.__Config.ACCESS_TOKEN if self.__Config.ACCESS_TOKEN != "" else None,
            project_number=self.__Config.GCP_PROJECT_NUMBER,
            endpoint_id=self.__Config.GCP_ENDPOINT_ID,
        )
        self.__TaskQueueManager = TaskQueueManager()
        self.__LineConnection = LineConnection(
                self.__Config.LINE_CHANNEL_SECRET,
                self.__Config.LINE_LINE_CHANNEL_ACCESS_TOKEN,
            )

    def Config(self) -> _Config:
        return self.__Config

    def GCPVertexAI(self) -> GCPVertexAI:
        return self.__GCPVertexAI

    def TaskQueueManager(self) -> TaskQueueManager:
        return self.__TaskQueueManager
    
    def LineConnection(self) -> LineConnection:
        return self.__LineConnection


container = _Container()


def get_container() -> _Container:
    return container
