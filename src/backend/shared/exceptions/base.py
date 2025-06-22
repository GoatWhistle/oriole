from fastapi import status


class AppException(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Application error"

    def __init__(self, status_code: int | None = None, detail: str | None = None):
        if status_code:
            self.status_code = status_code
        if detail:
            self.detail = detail
