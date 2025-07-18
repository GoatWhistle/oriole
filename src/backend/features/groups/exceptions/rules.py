from shared.exceptions import RuleException


class AccountAlreadyInSpaceException(RuleException):
    detail = "User already has an account in the group"
