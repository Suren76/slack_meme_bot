import requests
from flask import Flask, request

from config import TOKEN, DEBUG

HOST = "localhost"
PORT = 880

BASEURL_SERVICE = "localhost"
PORT_SERVICE = "5555"
HANDLER_SERVICE = f"http://{BASEURL_SERVICE+(':'+PORT_SERVICE if len(PORT_SERVICE) > 0 else '')}/handler"

app = Flask(__name__)


def _is_url_instagram_post_link(url: str) -> bool:
    if "https://www.instagram.com" in url:
        endpoint = url.split("https://www.instagram.com")[1]
        post_type = endpoint.split("/")[1]
        if post_type is not None:
            if post_type in ["reel", "p"]:
                return True

    return False


message_id = {"last_message_id": ""}


@app.route('/bot', methods=['GET', 'POST'])
def bot():
    if request.method == "POST":
        if len(request.json) == 3:
            return request.json["challenge"]

        current_message_id = request.json["event"].get("client_msg_id")

        if current_message_id is not None:
            if message_id["last_message_id"] != current_message_id:

                message_id["last_message_id"] = current_message_id

                message_text = request.json["event"]["blocks"][0]["elements"][0]["elements"][0].get("url") if _is_url_instagram_post_link(request.json["event"]["blocks"][0]["elements"][0]["elements"][0].get("url")) else None
                message_type = request.json["event"]["blocks"][0]["type"] == "rich_text"
                # message_id = request.json["event"]["client_msg_id"][0]["type"] == "rich_text"
                message_text_type = request.json["event"]["blocks"][0]["elements"][0]["elements"][0]["type"] == "link"

                print(f"{message_type=}")
                print(f"{message_text=}")
                print(f"{message_text_type=}")

                if bool(message_text is not None) and message_type and message_text_type:
                    print("condition ok")
                    dict_to_send = {
                        "channel": request.json["event"]["channel"],
                        "url": message_text,
                        "message_id": current_message_id
                    }
                    requests.post(HANDLER_SERVICE, json=dict_to_send)

    return "OK"


app.run(debug=DEBUG, host=HOST, port=PORT)

