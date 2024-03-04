import queue
import ngrok
from api.server import Server
from cli.command_interface import CommandInterface
from config import get_config
from model.gcp import GCPVertexAI
from model.task import TaskQueueManager


class ApiServerStartCommand(CommandInterface):
    vertex_ai = GCPVertexAI(
        project_number=get_config().GCP_PROJECT_NUMBER,
        endpoint_id=get_config().GCP_ENDPOINT_ID,
    )
    queue_manager = TaskQueueManager()

    def execute(self, ngrok_ingress: bool):
        app = Server(vertex_ai=self.vertex_ai, queue_manager=self.queue_manager)

        if ngrok_ingress:
            listener = ngrok.forward(get_config().SERVER_PORT, authtoken_from_env=True)
            print(f"Ingress established at {listener.url()}")

            app.start(get_config().SERVER_PORT, debug=False)

        else:
            app.start(get_config().SERVER_PORT)
