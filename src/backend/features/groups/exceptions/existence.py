from features.spaces.exceptions import SpaceNotFoundException
from shared.exceptions import NotFoundException


class GroupNotFoundException(SpaceNotFoundException):
    detail = "Group not found"


class GroupInviteNotFoundException(NotFoundException):
    detail = "Group invite not found"


class AccountNotFoundInSpaceException(NotFoundException):
    detail = "User does not have an account in the group"
