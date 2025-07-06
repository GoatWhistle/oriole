from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from features.groups.models import GroupInvite
from utils import get_current_utc


async def create_group_invite(
    session: AsyncSession,
    group_id: int,
    code: str,
    expires_minutes: int,
) -> GroupInvite:
    invite = GroupInvite(
        code=code,
        space_id=group_id,
        expires_at=get_current_utc(offset_minutes=expires_minutes),
        is_active=True,
    )
    session.add(invite)
    await session.commit()
    await session.refresh(invite)
    return invite


async def get_group_invite_by_code(
    session: AsyncSession,
    code: str,
) -> GroupInvite | None:
    result = await session.execute(select(GroupInvite).where(GroupInvite.code == code))
    return result.scalars().first()


async def set_invite_inactive(
    session: AsyncSession,
    invite: GroupInvite,
) -> None:
    invite.is_active = False
    await session.commit()


async def delete_group_invites_by_group_id(
    session: AsyncSession,
    group_id: int,
) -> None:
    await session.execute(delete(GroupInvite).where(GroupInvite.space_id == group_id))
