import os
import sys
import threading
from wsgiref.simple_server import make_server
from flask import url_for
from api.server import Server
from cli.command_interface import CommandInterface


class RouteListCommand(CommandInterface):

    def execute(self):
        server = Server()
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
