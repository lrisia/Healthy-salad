from asyncio import sleep
import os
from dotenv import load_dotenv

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"


if __name__ == "__main__":
    load_dotenv()
    app.run(host="0.0.0.0", port=int(os.environ.get("SERVER_PORT", 8080)))
