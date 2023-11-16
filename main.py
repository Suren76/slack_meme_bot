import os

from flask import Flask

from config import SOLID_MICROSERVICE_CONFIGS, DEBUG

from handler import service_handler
from bot_events import service_bot_events
from setup import setup

HOST = SOLID_MICROSERVICE_CONFIGS["HOST"]
PORT = SOLID_MICROSERVICE_CONFIGS["PORT"]


def main():
    setup()
    app = Flask(__name__)

    app.register_blueprint(service_handler)
    app.register_blueprint(service_bot_events)

    app.run(debug=DEBUG, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

