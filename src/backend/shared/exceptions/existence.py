from fastapi import status

from shared.exceptions import AppException


class NotFoundException(AppException):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "Object not found"
