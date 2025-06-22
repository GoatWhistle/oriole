from fastapi import status

from shared.exceptions import AppException


class RoleException(AppException):
    status_code = status.HTTP_403_FORBIDDEN
