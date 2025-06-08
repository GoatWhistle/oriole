from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from groups.models import GroupInvite
from utils import get_current_utc


async def check_invite_active(
    invite: GroupInvite,
) -> None:
    if not invite.is_active:
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail="Invite code is no longer active"
        )


async def check_invite_not_expired(
    invite: GroupInvite,
) -> None:
    if invite.expires_at < get_current_utc():
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail="Invite code has expired"
        )


async def validate_invite_code(
    session: AsyncSession,
    code: str,
) -> GroupInvite:
    invite = await session.execute(select(GroupInvite).where(GroupInvite.code == code))
    invite = invite.scalars().first()

    if not invite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid invite code"
        )

    await check_invite_active(invite=invite)
    await check_invite_not_expired(invite=invite)

    return invite
