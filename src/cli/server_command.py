import queue
from flask import url_for
import ngrok
import schedule
from api.server import Server
from cli.command_interface import CommandInterface
from model.config import get_config
from model.gcp import GCPVertexAI
from model.task import TaskQueueManager


class StartApiServerCommand(CommandInterface):
    def __init__(self, ngrok_ingress_activate: bool) -> None:
        self.__ngrok_ingress_activate = ngrok_ingress_activate

    def execute(self, container):
        app = Server(container=container)

        if self.__ngrok_ingress_activate:
            listener = ngrok.forward(get_config().SERVER_PORT, authtoken_from_env=True)
            print(f"Ingress established at {listener.url()}")

            app.start(get_config().SERVER_PORT, debug=False)

        else:
            app.start(get_config().SERVER_PORT)


class ListAllRouteCommand(CommandInterface):
    def execute(self, container):
        server = Server(container=container)
        app = server.server

        with app.app_context(), app.test_request_context():
            for rule in app.url_map.iter_rules():
                if rule.methods is None:
                    continue
                options = {}
                for arg in rule.arguments:
                    options[arg] = "[{0}]".format(arg)

                url = url_for(rule.endpoint, **options)
                method = next(
                    (
                        method
                        for method in rule.methods
                        if method in ["GET", "POST", "PUT", "DELETE"]
                    ),
                    "",
                )
                print("{:>7s}: {:50s} at {}".format(method, url, rule.endpoint))


class StartAllAppCommand(CommandInterface):
    # def _do_task(self):
    #     if self.queue_manager.is_empty():
    #         print("No task to do")
    #         return

    #     task = self.queue_manager.get()
    #     data = self.queue_manager.load_image(task.image_path)
    #     result = self.vertex_ai.vertex_ai_predict(
    #         data.tolist(), self.config.GCP_PROJECT_NUMBER, self.config.GCP_ENDPOINT_ID
    #     )
    #     print(result)

    def execute(self, container):
        pass

    #     app = Server(queue_manager=self.queue_manager, vertex_ai=self.vertex_ai)
    #     app.start(get_config().SERVER_PORT, debug=False)

    #     schedule.every(10).second.do(self._do_task)
