from shared.exceptions import AuthException, AuthForbiddenException


class AuthenticationRequiredException(AuthException):
    detail = "Authentication required"


class AuthenticatedForbiddenException(AuthForbiddenException):
    detail = "Authenticated users cannot perform this action"
