from typing import Optional
from slack_sdk import WebClient
from config import TOKEN


def send_message(channel: str, content: bytes, comment: Optional[str] = None, client: Optional[WebClient] = None) -> None:
    if client is None:
        client = WebClient(token=TOKEN["bot"], timeout=100)

    client.files_upload_v2(
        channel=channel,
        file=content,
        initial_comment=comment
    )
