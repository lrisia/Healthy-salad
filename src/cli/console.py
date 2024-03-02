import click
from cli.playground_command import PlaygroundCommand

from cli.route_list_command import RouteListCommand
from cli.server_start_command import ApiServerStartCommand


@click.group()
def console() -> None:
    pass


@console.command()
def pg() -> None:
    playground_command = PlaygroundCommand()
    playground_command.execute()


@console.command()
@click.option(
    "-N",
    "--ngrok",
    default=False,
    is_flag=True,
    type=bool,
    help="Use this option to start the server with ngrok ingress.",
)
def api_start(ngrok: bool) -> None:
    server_start_command = ApiServerStartCommand()
    server_start_command.execute(ngrok)


@console.command()
def route_list() -> None:
    route_list_command = RouteListCommand()
    route_list_command.execute()
