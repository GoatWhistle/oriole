from http import HTTPStatus

from shared.exceptions import AppException


class RuleException(AppException):
    status_code: int = HTTPStatus.FORBIDDEN
    detail: str = "Rule violation"


class InactiveObjectException(RuleException):
    detail: str = "Operation is not allowed on inactive object."
