from typing import TypeAlias, Literal, Optional

from requests import get

from exceptions import ContentDownloadException
from get_post_download_url import InstaDownloadLink

Video: TypeAlias = bytes
Image: TypeAlias = bytes


# generic kazmakerpi
def download_content(
        insta_download: Optional[InstaDownloadLink] = None,
        url: Optional[str] = None,
        content_type: Optional[Literal["video", "image"]] = None,
        filename: Optional[str] = None,
        save: Optional[bool] = True
) -> bytes:

    _content_type = content_type if content_type else insta_download.content_type
    _download_url = url if url else insta_download.download_url
    _filename = filename if save else ""

    if _content_type is None: raise ContentDownloadException(_content_type)
    if _download_url is None: raise ContentDownloadException(_content_type)
    if _filename is None: raise ContentDownloadException(_content_type)

    return _download_content(
        content_type=_content_type,
        url=_download_url,
        save=save,
        filename=_filename
    )


def download_video(url: str, save=True, filename="test_video.mp4") -> Video:
    return _download_content(
        content_type="video",
        url=url,
        save=save,
        filename=filename
    )


def download_photo(url: str, save=True, filename="test_image.jpeg") -> Image:
    return _download_content(
        content_type="image",
        url=url,
        save=save,
        filename=filename
    )


def _download_content(
        url: str,
        filename: str,
        content_type: Literal["video", "image"],
        save: bool
) -> bytes:

    content: bytes = get(url, stream=True).content

    if save:
        with open(filename, "wb+") as file:
            file.write(content)

    return content
