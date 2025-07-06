from http import HTTPStatus
from shared.exceptions import AppException


class NotFoundException(AppException):
    status_code: int = HTTPStatus.NOT_FOUND
    detail: str = "Object not found"


class BadRequest(AppException):
    detail: str = "Bad request"
