import json
from typing import Optional, TypeAlias

from pydantic import BaseModel, ValidationError, Field


class BaseBlock(BaseModel):
    # saxin getter setter kazmakerpi
    type: str
    style: Optional[dict] = None


class TextBlock(BaseBlock):
    text: str


class LinkBlock(BaseBlock):
    url: str


BlockTypes: TypeAlias = TextBlock | LinkBlock


class Element(BaseModel):
    type: str
    elements: list[BlockTypes]


class Block(BaseModel):
    type: str
    block_id: str
    elements: list[Element]


# normal anun mtaci
class BaseContentResponse(BaseModel):
    client_msg_id: str
    type: str
    text: str
    user: str
    ts: float
    blocks: list[Block]
    team: str


class Message(BaseContentResponse):
    pass


class Event(BaseContentResponse):
    channel: str
    event_ts: float
    channel_type: str


class SlackResponse(BaseModel):
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

    def get_message_id(self):
        return self.messages[0].client_msg_id


class EventResponse(BaseModel):
    token: str
    team_id: str
    context_team_id: str
    context_enterprise_id: Optional[str] = None
    api_app_id: str
    event: Event
    type: str
    event_id: str
    event_time: float
    authorizations: list[dict[str, object]]
    is_ext_shared_channel: bool
    event_context: str

    @property
    def get_items(self) -> list[BlockTypes]:
        return self.event.blocks[0].elements[0].elements

    @property
    def get_message_id(self) -> str:
        return self.event.client_msg_id



# test data
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


event_response_example = {
    'token': 'cO1IfBO1uIieET6hNYjCnlUq',
    'team_id': 'T05CG9PCRLN',
    'context_team_id': 'T05CG9PCRLN',
    'context_enterprise_id': None,
    'api_app_id': 'A060RL7RN6B',
    'event': {
        'client_msg_id': '73cf5e9a-c61c-4dc8-99ea-27a79f0001db',
        'type': 'message',
        'text': '<https://www.instagram.com/reel/Cyq8wvVufvc/?igshid=cW5pODlremY0MThs>',
        'user': 'U05D1J6GF5F',
        'ts': '1699969168.317269',
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
        'team': 'T05CG9PCRLN',
        'channel': 'C05C8D6NG9M',
        'event_ts': '1699969168.317269',
        'channel_type': 'channel'
    },
    'type': 'event_callback',
    'event_id': 'Ev066BCTV332',
    'event_time': 1699969168,
    'authorizations': [
        {
            'enterprise_id': None,
            'team_id': 'T05CG9PCRLN',
            'user_id': 'U05D1J6GF5F',
            'is_bot': False,
            'is_enterprise_install': False
        }
    ],
    'is_ext_shared_channel': False,
    'event_context': '4-eyJldCI6Im1lc3NhZ2UiLCJ0aWQiOiJUMDVDRzlQQ1JMTiIsImFpZCI6IkEwNjBSTDdSTjZCIiwiY2lkIjoiQzA1QzhENk5HOU0ifQ'
}


non_event_response_example = {
    'token': 'cO1IfBO1uIieET6hNYjCnlUq',
    'team_id': 'T05CG9PCRLN',
    'context_team_id': 'T05CG9PCRLN',
    'context_enterprise_id': None,
    'api_app_id': 'A060RL7RN6B',
    'event': {
        'type': 'message',
        'text': '',
        'files': [
            {
                'id': 'F065AAZRT47',
                'created': 1699991537,
                'timestamp': 1699991537,
                'name': 'Uploaded file',
                'title': 'Uploaded file',
                'mimetype': 'video/mp4',
                'filetype': 'mp4',
                'pretty_type': 'MPEG 4 Video',
                'user': 'U06163S6B27',
                'user_team': 'T05CG9PCRLN',
                'editable': False,
                'size': 1089405,
                'mode': 'hosted',
                'is_external': False,
                'external_type': '',
                'is_public': False,
                'public_url_shared': False,
                'display_as_bot': False,
                'username': '',
                'transcription': {
                    'status': 'processing'
                },
                'mp4': 'https://files.slack.com/files-tmb/T05CG9PCRLN-F065AAZRT47-3679de5e07/uploaded_file.mp4',
                'url_private': 'https://files.slack.com/files-tmb/T05CG9PCRLN-F065AAZRT47-3679de5e07/uploaded_file.mp4',
                'url_private_download': 'https://files.slack.com/files-pri/T05CG9PCRLN-F065AAZRT47/download/uploaded_file',
                'mp4_low': 'https://files.slack.com/files-tmb/T05CG9PCRLN-F065AAZRT47-3679de5e07/uploaded_file_trans.mp4',
                'media_display_type': 'video',
                'thumb_video': 'https://files.slack.com/files-tmb/T05CG9PCRLN-F065AAZRT47-3679de5e07/uploaded_file_thumb_video.jpeg',
                'thumb_video_w': 720,
                'thumb_video_h': 1280,
                'permalink': 'https://for-testglobal.slack.com/files/U06163S6B27/F065AAZRT47/uploaded_file',
                'permalink_public': 'https://slack-files.com/T05CG9PCRLN-F065AAZRT47-49a272fe2c',
                'has_rich_preview': False,
                'file_access': 'visible'
            }
        ],
        'upload': True,
        'user': 'U06163S6B27',
        'display_as_bot': False,
        'ts': '1699991544.584639',
        'bot_id': 'B060RL8EXFH',
        'channel': 'C05C8D6NG9M',
        'subtype': 'file_share',
        'event_ts': '1699991544.584639',
        'channel_type': 'channel'
    },
    'type': 'event_callback',
    'event_id': 'Ev066DS9DH8Q',
    'event_time': 1699991544,
    'authorizations': [
        {
            'enterprise_id': None,
            'team_id': 'T05CG9PCRLN',
            'user_id': 'U05D1J6GF5F',
            'is_bot': False,
            'is_enterprise_install': False
        }
    ],
    'is_ext_shared_channel': False,
    'event_context': '4-eyJldCI6Im1lc3NhZ2UiLCJ0aWQiOiJUMDVDRzlQQ1JMTiIsImFpZCI6IkEwNjBSTDdSTjZCIiwiY2lkIjoiQzA1QzhENk5HOU0ifQ'
}

if __name__ == "__main__":
    try:
        print(EventResponse.model_validate_json(json.dumps(event_response_example)))
    except ValidationError as e:
        print(e.json())
        print(e.errors())

