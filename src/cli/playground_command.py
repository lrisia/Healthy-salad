from cli.command_interface import CommandInterface


class PlaygroundCommand(CommandInterface):

    def execute(self):
        print("Welcome to playground!")
