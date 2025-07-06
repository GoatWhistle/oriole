from http import HTTPStatus

from shared.exceptions import AppException


class TelegramAuthException(AppException):
    status_code: int = HTTPStatus.BAD_REQUEST
    detail: str = "Telegram auth failed"
