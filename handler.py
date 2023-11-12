from flask import Flask, request

from download_content import download_content
from get_post_download_url import get_post_download_url
from post_message import send_message

from config import DEBUG


HOST = "localhost"
PORT = 5555

app = Flask(__name__)


@app.route("/handler", methods=["POST"])
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
    app.run(debug=DEBUG, host=HOST, port=PORT)
