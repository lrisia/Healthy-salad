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
