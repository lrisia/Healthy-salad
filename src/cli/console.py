from tracemalloc import start
from typing import Container
import click
from cli.playground_command import PlaygroundCommand

from cli.server_command import ListAllRouteCommand, StartApiServerCommand, StartAllAppCommand
from model.config import get_config
from model.container import get_container
from model.gcp import GCPVertexAI
from model.task import TaskQueueManager


@click.group()
def console() -> None:
    pass


@console.command("pg", short_help="Start the playground for test anything.")
def pg() -> None:
    playground_command = PlaygroundCommand()
    playground_command.execute()


@console.command("server:start", short_help="Start api server.")
@click.option(
    "-N",
    "--ngrok",
    default=False,
    is_flag=True,
    type=bool,
    help="Use this option to start the server with ngrok ingress for get temporary public domain name.",
)
def start_server(ngrok: bool) -> None:
    start_server_command = StartApiServerCommand(ngrok)
    start_server_command.execute(get_container())


@console.command("route:list", short_help="List all available routes.")
def route_list() -> None:
    list_all_route_command = ListAllRouteCommand()
    list_all_route_command.execute(get_container())


@console.command(
    "start:all", short_help="Start all application. Run in full mode. API and Cron"
)
def start_all() -> None:
    start_all_app_command = StartAllAppCommand()
    start_all_app_command.execute(get_container())
