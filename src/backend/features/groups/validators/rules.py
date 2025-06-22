from datetime import datetime

from features.groups.exceptions import (
    GroupInviteInactiveException,
    GroupInviteExpiredException,
)
from utils import get_current_utc


def check_group_invite_active(
    group_invite_is_active: bool,
) -> None:
    if not group_invite_is_active:
        raise GroupInviteInactiveException()


def check_group_invite_not_expired(
    group_invite_expires_at: datetime,
) -> None:
    if group_invite_expires_at < get_current_utc():
        raise GroupInviteExpiredException()
