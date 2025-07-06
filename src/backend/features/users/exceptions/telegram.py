from http import HTTPStatus

from shared.exceptions import TelegramAuthException


class MissingHashException(TelegramAuthException):
    detail = "Missing Telegram auth hash"


class InvalidHashException(TelegramAuthException):
    status_code: int = HTTPStatus.FORBIDDEN
    detail: str = "Invalid Telegram auth hash"


class ExpiredAuthException(TelegramAuthException):
    status_code: int = HTTPStatus.FORBIDDEN
    detail: str = "Telegram auth data expired (more than 24h)"
