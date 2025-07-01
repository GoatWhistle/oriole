from shared.exceptions import AuthException


class AuthenticationRequiredException(AuthException):
    detail = "Authentication required"


class AuthenticatedForbiddenException(AuthenticationRequiredException):
    detail = "Authenticated users cannot perform this action"
