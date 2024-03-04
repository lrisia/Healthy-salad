import schedule
from api.server import Server
from cli.command_interface import CommandInterface
from config import get_config
from model.gcp import GCPVertexAI

from model.task import TaskQueueManager


class StartAllAppCommand(CommandInterface):
    vertex_ai = GCPVertexAI()
    queue_manager = TaskQueueManager()
    config = get_config()

    def _do_task(self):
        if self.queue_manager.is_empty():
            print("No task to do")
            return

        task = self.queue_manager.get()
        data = self.queue_manager.load_image(task.image_path)
        result = self.vertex_ai.vertex_ai_predict(
            data.tolist(), self.config.GCP_PROJECT_NUMBER, self.config.GCP_ENDPOINT_ID
        )
        print(result)

    def execute(self):
        app = Server(queue_manager=self.queue_manager, vertex_ai=self.vertex_ai)
        app.start(get_config().SERVER_PORT, debug=False)

        schedule.every(10).second.do(self._do_task)
