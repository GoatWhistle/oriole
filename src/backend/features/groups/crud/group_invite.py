from secrets import choice
from string import ascii_uppercase, digits
from typing import Any

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from database import DbHelper
from features.groups.models import GroupInvite
from features.groups.schemas import GroupInviteCreate
from utils import get_current_utc


async def generate_unique_group_invite_code(
    session: AsyncSession,
    length: int = 16,
) -> str:
    alphabet = ascii_uppercase + digits
    while True:
        code = "".join(choice(alphabet) for _ in range(length))
        result = await session.execute(
            select(GroupInvite).where(GroupInvite.code == code)
        )
        if not result.scalar_one_or_none():
            return code


async def create_group_invite(
    session: AsyncSession,
    group_invite_in: GroupInviteCreate,
    creator_id: int,
) -> GroupInvite:
    group_invite = GroupInvite(
        **group_invite_in.model_dump(),
        code=generate_unique_group_invite_code(session),
        creator_id=creator_id,
        created_at=get_current_utc(),
        user_usages=0,
        is_actuve=True,
    )
    session.add(group_invite)
    await session.commit()
    await session.refresh(group_invite)
    return group_invite


async def get_group_invites(
    session: AsyncSession,
    is_active: bool | None = None,
) -> list[GroupInvite]:
    statement = select(GroupInvite)
    if is_active is not None:
        statement = statement.where(GroupInvite.is_active == is_active)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_group_invite_by_id(
    session: AsyncSession,
    group_invite_id: int,
) -> GroupInvite | None:
    return await session.get(GroupInvite, group_invite_id)


async def get_group_invites_by_group_id(
    session: AsyncSession,
    group_id: int,
    is_active: bool | None = None,
) -> list[GroupInvite]:
    statement = select(GroupInvite).where(GroupInvite.space_id == group_id)
    if is_active is not None:
        statement = statement.where(GroupInvite.is_active == is_active)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_group_invite_by_code(
    session: AsyncSession,
    code: str,
) -> GroupInvite | None:
    result = await session.execute(select(GroupInvite).where(GroupInvite.code == code))
    return result.scalars().first()


async def update_group_invite(
    session: AsyncSession,
    group_invite: GroupInvite,
    group_invite_update: dict[str, Any],
) -> GroupInvite:
    for key, value in group_invite_update.items():
        setattr(group_invite, key, value)
    await session.commit()
    await session.refresh(group_invite)
    return group_invite


async def update_group_invites_activity():
    local_db_helper = DbHelper(url=str(settings.db.url))

    async with local_db_helper.session_factory() as session:
        group_invites = await get_group_invites(session)

        updated = False
        for group_invite in group_invites:
            if group_invite.expires_at is None:
                continue
            new_status = group_invite.expires_at <= get_current_utc()
            if group_invite.is_active != new_status:
                group_invite.is_active = new_status
                updated = True

        if updated:
            await session.commit()

        await local_db_helper.dispose()


async def delete_group_invite(
    session: AsyncSession,
    group_invite: GroupInvite,
) -> None:
    await session.delete(group_invite)
    await session.commit()


async def delete_group_invites_by_group_id(
    session: AsyncSession,
    group_id: int,
    is_active: bool | None = None,
) -> None:
    statement = delete(GroupInvite).where(GroupInvite.space_id == group_id)
    if is_active is not None:
        statement = statement.where(GroupInvite.is_active == is_active)
    await session.execute(statement)
    await session.commit()
