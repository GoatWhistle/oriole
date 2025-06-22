from shared.exceptions import RuleException, InactiveObjectException


class AccountAlreadyInGroupException(RuleException):
    detail = "User already has an account in the group"


class GroupInviteInactiveException(InactiveObjectException):
    detail = "Invite code is no longer active."


class GroupInviteExpiredException(InactiveObjectException):
    detail = "Invite code has expired."
