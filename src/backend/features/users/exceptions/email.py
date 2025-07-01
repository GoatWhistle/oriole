from shared.exceptions import RuleException


class EmailRequiredExceptions(RuleException):
    detail = "Email in the field required"


class EmailMismatchException(RuleException):
    detail = "Current email does not match token"
