from typing import Type

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from features.groups.models import Group, GroupInvite


async def get_group_if_exists(
    session: AsyncSession,
    group_id: int | Mapped[int],
) -> Group | Type[Group]:
    group = await session.get(Group, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group {group_id} does not exist",
        )
    return group


async def check_invite_exists(
    session: AsyncSession,
    code: str,
) -> GroupInvite | Type[GroupInvite]:
    result = await session.execute(select(GroupInvite).where(GroupInvite.code == code))
    invite = result.scalars().first()

    if not invite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invite code {code} does not exist",
        )
    return invite
