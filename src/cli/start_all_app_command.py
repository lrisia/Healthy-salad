from api.server import Server
from cli.command_interface import CommandInterface
from config import get_config
from model.gcp import CredentialManager


class StartAllAppCommand(CommandInterface):

    def execute(self):
        credential_manager = CredentialManager()

        app = Server(credential_manager=credential_manager)
        app.start(get_config().SERVER_PORT, debug=False)
        
        
