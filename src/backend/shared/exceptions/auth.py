from fastapi import status

from shared.exceptions import AppException


class AuthException(AppException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Unauthorized"
