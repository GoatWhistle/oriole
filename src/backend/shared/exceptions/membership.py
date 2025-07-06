from http import HTTPStatus

from shared.exceptions import AppException


class RoleException(AppException):
    status_code: int = HTTPStatus.FORBIDDEN
