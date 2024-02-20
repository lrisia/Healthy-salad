import click

from cli.route_list_command import RouteListCommand
from cli.server_start_command import ApiServerStartCommand

@click.group()
def console():
    pass
  
@console.command()
def api_start():
    server_start_command = ApiServerStartCommand()
    server_start_command.execute()
      
@console.command()
def route_list():
    route_list_command = RouteListCommand()
    route_list_command.execute()