from api.server import Server
from cli.command_interface import Command
from config import get_config


class ApiServerStartCommand(Command):
  
    def execute(self):
        app = Server()
        app.start(get_config().SERVER_PORT)
      