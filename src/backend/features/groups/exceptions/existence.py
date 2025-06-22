from shared.exceptions import NotFoundException


class GroupNotFoundException(NotFoundException):
    detail = "Group not found"


class GroupInviteNotFoundException(NotFoundException):
    detail = "Group invite not found"


class AccountNotFoundInGroupException(NotFoundException):
    detail = "User does not have an account in the group"
