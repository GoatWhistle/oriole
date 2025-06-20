from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from features.groups.models import GroupInvite
from features.groups.validators import get_group_invite_if_exists
from utils import get_current_utc


def check_group_invite_active(
    group_invite_is_active: bool,
) -> None:
    if not group_invite_is_active:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Invite code is no longer active",
        )


def check_group_invite_not_expired(
    group_invite_expires_at: datetime,
) -> None:
    if group_invite_expires_at < get_current_utc():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Invite code has expired",
        )


async def get_group_invite_if_valid(
    session: AsyncSession,
    code: str,
) -> GroupInvite:
    group_invite = await get_group_invite_if_exists(session, code)

    check_group_invite_active(group_invite.is_active)
    check_group_invite_not_expired(group_invite.expires_at)

    return group_invite
