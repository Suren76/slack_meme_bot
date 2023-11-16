import json

import requests
from flask import Flask, request, Blueprint

from config import DEBUG, MICROSERVICE_HANDLER, MICROSERVICE_BOT_EVENTS
from response_models import EventResponse

HOST = MICROSERVICE_BOT_EVENTS["HOST"]
PORT = MICROSERVICE_BOT_EVENTS["PORT"]

BASEURL_SERVICE = MICROSERVICE_HANDLER["HOST"]
PORT_SERVICE = str(MICROSERVICE_HANDLER["PORT"])

HANDLER_SERVICE = f"http://{BASEURL_SERVICE+(':'+PORT_SERVICE if len(PORT_SERVICE) > 0 else '')}/handler"


service_bot_events = Blueprint("bot", __name__)


def _is_url_instagram_post_link(url: str) -> bool:
    if "https://www.instagram.com" in url:
        endpoint = url.split("https://www.instagram.com")[1]
        post_type = endpoint.split("/")[1]
        if post_type is not None:
            if post_type in ["reel", "p"]:
                return True

    return False


message_id = {"last_message_id": ""}


@service_bot_events.route('/bot', methods=['GET', 'POST'])
def bot():
    if request.method == "POST":
        # verifying url for bot event subscription
        if len(request.json) == 3:
            return request.json["challenge"]

        # main
        if request.json["event"].get("files") is not None:
            return "", 200

        res = EventResponse.model_validate_json(json.dumps(request.json))
        current_message_id = res.get_message_id

        if current_message_id is not None:
            if message_id["last_message_id"] != current_message_id:
                message_id["last_message_id"] = current_message_id

                message_text = res.get_items[0].url if _is_url_instagram_post_link(res.get_items[0].url) else None
                message_text_type = res.get_items[0].type == "link"

                if bool(message_text is not None) and message_text_type:
                    dict_to_send = {
                        "channel": res.event.channel,
                        "url": message_text,
                        "message_id": current_message_id
                    }
                    requests.post(HANDLER_SERVICE, json=dict_to_send)

    return "OK", 200


if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(service_bot_events)
    app.run(debug=DEBUG, host=HOST, port=PORT)

