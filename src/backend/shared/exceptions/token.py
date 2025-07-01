from shared.exceptions import AppException


class InvalidTokenException(AppException):
    detail = "Token invalid"


class MissingTokenException(InvalidTokenException):
    detail = "Token is missing"
