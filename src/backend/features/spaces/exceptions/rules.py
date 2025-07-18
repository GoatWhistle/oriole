from shared.exceptions import InactiveObjectException


class SpaceInviteInactiveException(InactiveObjectException):
    detail = "Invite is no longer active."
