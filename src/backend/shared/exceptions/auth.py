from http import HTTPStatus

from shared.exceptions import AppException


class AuthException(AppException):
    status_code: int = HTTPStatus.UNAUTHORIZED
    detail: str = "Unauthorized"


class AuthForbiddenException(AppException):
    status_code: int = HTTPStatus.METHOD_NOT_ALLOWED
    detail: str = "Authorized"
