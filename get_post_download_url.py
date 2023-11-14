from dataclasses import dataclass

from instaloader import Post, Instaloader
from typing import Literal, NamedTuple
from exceptions import InvalidUrlException


@dataclass
class InstaLink:
    _url: str = None
    shortcode: str = None

    _BASE_URL: str = "https://www.instagram.com"

    @staticmethod
    def get_from(url):
        return InstaLink(
            _url=url,
            shortcode=url.split("/")[4]
        )

    @property
    def url(self):
        return f"{self._BASE_URL}/p/{self.shortcode}"


class InstaDownloadLink(NamedTuple):
    download_url: str
    content_type: Literal["video", "image"]


def _get_download_url(shortcode: str) -> InstaDownloadLink:
    post_to_download = Post.from_shortcode(Instaloader().context, shortcode)

    _content_type: Literal["video", "image"] = "video" if post_to_download.is_video==True else "image"  # PY-44103
    _download_url = post_to_download.video_url if _content_type == "video" else post_to_download.url

    return InstaDownloadLink(_download_url, _content_type)


def get_post_download_url(
        url: str = None,
        shortcode: str = None,
) -> InstaDownloadLink:

    if url is None and shortcode is None:
        raise InvalidUrlException(f"url: {url}, shortcode: {shortcode}")

    _shortcode: str = (InstaLink(shortcode=shortcode) if shortcode else InstaLink.get_from(url)).shortcode
    _link = _get_download_url(_shortcode)

    return _link
