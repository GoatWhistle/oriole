from shared.exceptions import RuleException


class UserNotFoundException(RuleException):
    detail = "Group not found"


class ProfileNotFoundException(RuleException):
    detail = "User profile not found"
