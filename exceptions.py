from typing_extensions import override


class BotBaseException(Exception):
    ...


class InvalidUrlException(BotBaseException):
    ...


class ContentDownloadException(BotBaseException):
    ...
