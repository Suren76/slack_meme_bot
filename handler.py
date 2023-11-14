from flask import Flask, request, Blueprint

from download_content import download_content
from get_post_download_url import get_post_download_url
from post_message import send_message

from config import DEBUG, MICROSERVICE_HANDLER


HOST = MICROSERVICE_HANDLER["HOST"]
PORT = MICROSERVICE_HANDLER["PORT"]


service_handler = Blueprint("handler", __name__)


@service_handler.route("/handler", methods=["POST"])
def handler():
    data = request.json

    url_from_messages = get_post_download_url(data["url"])
    content = download_content(url_from_messages, save=False)
    send_message(
        channel=data["channel"],
        content=content
    )

    return "200", 200


if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(service_handler)
    app.run(debug=DEBUG, host=HOST, port=PORT)
