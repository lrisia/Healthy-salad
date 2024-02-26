import ngrok
from api.server import Server
from cli.command_interface import Command
from config import get_config


class ApiServerStartCommand(Command):
  
    def execute(self, ngrok_ingress: bool):
        app = Server()
        
        if (ngrok_ingress):
            listener = ngrok.forward(get_config().SERVER_PORT, authtoken_from_env=True)
            print(f"Ingress established at {listener.url()}")
         
            app.start(get_config().SERVER_PORT, debug=False)
        
        else:
            app.start(get_config().SERVER_PORT)
      