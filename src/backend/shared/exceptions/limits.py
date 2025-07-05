from http import HTTPStatus
from shared.exceptions import AppException


class LimiterException(AppException):
    status_code: int = HTTPStatus.BAD_REQUEST
    detail: str = "Rate limiter error"


class RateLimitException(LimiterException):
    status_code: int = HTTPStatus.TOO_MANY_REQUESTS
    detail: str = "Rate limit exceeded"

    def __init__(self, retry_after: int = 60, detail: str | None = None):
        super().__init__(detail=detail)
        self.retry_after = retry_after
