from flask import Flask

class Server:
    server: Flask = Flask(__name__)

    def __init__(self, port: int):
        self.port = port

    def start(self):
        self.app.run(host=self.host, port=self.port)