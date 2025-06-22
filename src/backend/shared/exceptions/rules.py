from fastapi import status

from shared.exceptions import AppException


class RuleException(AppException):
    status_code: int = status.HTTP_403_FORBIDDEN
    detail: str = "Rule violation"


class InactiveObjectException(RuleException):
    detail: str = "Operation is not allowed on inactive object."
