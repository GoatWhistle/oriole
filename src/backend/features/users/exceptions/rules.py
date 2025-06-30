from shared.exceptions import RuleException


class UserAlreadyRegisteredException(RuleException):
    detail = "User is already registered"


class EmailAlreadyRegisteredException(RuleException):
    detail = "Email is already registered"


class InvalidCredentialsException(RuleException):
    detail = "Invalid login or password"


class PasswordMatchException(RuleException):
    detail = "The new password must be different from the previous one"
