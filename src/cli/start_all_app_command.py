import queue
from cv2 import line
import ngrok
import schedule
from api.server import Server
from cli.command_interface import CommandInterface
from model.config import get_config
from model.container import _Container
from model.gcp import GCPVertexAI

from model.task import TaskQueueManager
from utils.image import preprocess_image


class StartAllAppCommand(CommandInterface):
    def __init__(self, ngrok_ingress_activate: bool) -> None:
        self.__ngrok_ingress_activate = ngrok_ingress_activate
    
    def _do_task(self, container: _Container):
        print("Start do task")
        queue_manager = container.TaskQueueManager()
        gcp_vertex_ai = container.GCPVertexAI()
        line_connection = container.LineConnection()
        if queue_manager.is_empty():
            print("No task to do")
            return

        task = queue_manager.get()
        # data = line_connection.get_content(task.image_id)
        # result = gcp_vertex_ai.predict(data.tolist())
        # line_connection.send_message(task.user_id, result)
        line_connection.send_message(task.user_id, "eiei")
        # print(result)

    def execute(self, container):
        app = Server(container=container)
        
        if self.__ngrok_ingress_activate:
            listener = ngrok.forward(get_config().SERVER_PORT, authtoken_from_env=True)
            print(f"Ingress established at {listener.url()}")
            
        app.start(container.Config().SERVER_PORT, debug=False)

        schedule.every(10).seconds.do(self._do_task, container=container)
        while True:
            schedule.run_pending()
