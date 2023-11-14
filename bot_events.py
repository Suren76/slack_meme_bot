from pydantic import BaseModel
from typing import Optional

import requests
from flask import Flask, request, Blueprint

from config import DEBUG, MICROSERVICE_HANDLER, MICROSERVICE_BOT_EVENTS


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

                if bool(message_text is not None) and message_type and message_text_type:
                    dict_to_send = {
                        "channel": request.json["event"]["channel"],
                        "url": message_text,
                        "message_id": current_message_id
                    }
                    requests.post(HANDLER_SERVICE, json=dict_to_send)

    return "OK"


if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(service_bot_events)
    app.run(debug=DEBUG, host=HOST, port=PORT)


input_example = {
    'ok': True,
    'messages': [
        {
            'client_msg_id': '7f80cb91-d831-4f10-9ad9-5a839544a640',
            'type': 'message',
            'text': '<https://www.instagram.com/reel/Cyq8wvVufvc/?igshid=cW5pODlremY0MThs>',
            'user': 'U05D1J6GF5F',
            'ts': '1699908476.852299',
            'blocks': [
                {
                    'type': 'rich_text',
                    'block_id': 'A3ULD',
                    'elements': [
                        {
                            'type': 'rich_text_section',
                            'elements': [
                                {
                                    'type': 'link',
                                    'url': 'https://www.instagram.com/reel/Cyq8wvVufvc/?igshid=cW5pODlremY0MThs'
                                }
                            ]
                        }
                    ]
                }
            ],
            'team': 'T05CG9PCRLN'
        }
    ],
    'has_more': True,
    'is_limited': False,
    'pin_count': 0,
    'channel_actions_ts': None,
    'channel_actions_count': 0,
    'response_metadata': {
        'next_cursor': 'bmV4dF90czoxNjk5OTA4Mzk3MTk5NjI5'
    }
}

complex_input_example = {
    'ok': True,
    'messages': [
        {
            'client_msg_id': '182bf584-ea4f-4187-bf12-22a69ea690d7',
            'type': 'message',
            'text': '4154654\n<https://www.instagram.com/reel/Cyq8wvVufvc/?igshid=cW5pODlremY0MThs>\n*4545*\n_888888888_',
            'user': 'U05D1J6GF5F',
            'ts': '1699916839.290609',
            'blocks': [
                {
                    'type': 'rich_text',
                    'block_id': 'kVjci',
                    'elements': [
                        {
                            'type': 'rich_text_section',
                            'elements': [
                                {
                                    'type': 'text',
                                    'text': '4154654\n'
                                },
                                {
                                    'type': 'link',
                                    'url': 'https://www.instagram.com/reel/Cyq8wvVufvc/?igshid=cW5pODlremY0MThs'
                                },
                                {
                                    'type': 'text',
                                    'text': '\n'
                                },
                                {
                                    'type': 'text',
                                    'text': '4545',
                                    'style': {
                                        'bold': True
                                    }
                                },
                                {
                                    'type': 'text',
                                    'text': '\n'
                                }, {
                                    'type': 'text',
                                    'text': '888888888',
                                    'style': {
                                        'italic': True
                                    }
                                }
                            ]
                        }
                    ]
                }
            ],
            'team': 'T05CG9PCRLN'
        }
    ],
    'has_more': True,
    'is_limited': False,
    'pin_count': 0,
    'channel_actions_ts': None,
    'channel_actions_count': 0,
    'response_metadata': {
        'next_cursor': 'bmV4dF90czoxNjk5OTE2NzkwMjUwNzE5'
    }
}
