from features.spaces.exceptions.rules import SpaceInviteInactiveException


def check_space_invite_active(is_active: bool) -> None:
    if not is_active:
        raise SpaceInviteInactiveException()
