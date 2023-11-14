import json
from typing import Optional

from pydantic import BaseModel, ValidationError, Field


class BaseBlock(BaseModel):
    type: str
    style: Optional[dict] = None


class TextBlock(BaseBlock):
    text: str


class LinkBlock(BaseBlock):
    url: str


class Element(BaseModel):
    type: str
    elements: list[TextBlock | LinkBlock]


class Block(BaseModel):
    type: str
    block_id: str
    elements: list[Element]


class Message(BaseModel):
    client_msg_id: str
    type: str
    text: str
    user: str
    ts: float
    blocks: list[Block]
    team: str


class SlackResponseV(BaseModel):
    ok: bool
    messages: list[Message]
    has_more: bool
    is_limited: bool
    pin_count: int
    channel_actions_ts: Optional[int]
    channel_actions_count: Optional[int]
    response_metadata: dict[str, str]

    def get_items(self):
        return self.messages[0].blocks[0].elements[0].elements



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


try:
    print(Message.model_validate_json(json.dumps(complex_input_example)))
except ValidationError as e:
    print(e.json())
    print(e.errors())

