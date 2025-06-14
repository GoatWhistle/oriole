from secrets import choice
from string import ascii_uppercase, digits
from urllib.parse import urljoin

from fastapi import Request
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from features.groups.models import Account
from features.groups.models import GroupInvite
from features.groups.schemas import AccountRole
from features.groups.validators import (
    get_group_if_exists,
    check_admin_permission_in_group,
    check_user_in_group,
    validate_invite_code,
)
from features.users.validators import check_user_exists
from utils import get_current_utc


async def generate_unique_group_invite_code(
    session: AsyncSession,
    length: int = 7,
) -> str:
    alphabet = ascii_uppercase + digits
    while True:
        code = "".join(choice(alphabet) for _ in range(length))
        result = await session.execute(
            select(GroupInvite).where(GroupInvite.code == code)
        )
        if not result.scalar_one_or_none():
            return code


async def invite_user(
    session: AsyncSession,
    user_id: int,
    request: Request,
    group_id: int,
    expires_minutes: int,
    single_use: bool,
) -> dict:
    await check_admin_permission_in_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )

    code = await generate_unique_group_invite_code(session=session)
    code += "1" if single_use else "0"

    invite = GroupInvite(
        code=code,
        group_id=group_id,
        expires_at=get_current_utc(offset_minutes=expires_minutes),
        is_active=True,
    )

    session.add(invite)
    await session.commit()

    base_url = str(request.base_url)
    base_url = base_url[:-1] if base_url.endswith("/") else base_url

    return {"link": urljoin(base_url, f"/groups/join/{code}")}


async def join_by_link(
    session: AsyncSession,
    user_id: int,
    invite_code: str,
) -> dict:

    await check_user_exists(session=session, user_id=user_id)
    single_use = invite_code[-1] == "1"
    invite = await validate_invite_code(session, invite_code)
    group_id = invite.group_id

    await check_user_in_group(session, user_id, group_id, is_correct=False)

    existing_accounts = await session.execute(
        select(Account).where(Account.group_id == group_id)
    )
    role = (
        AccountRole.OWNER
        if not existing_accounts.scalars().all()
        else AccountRole.MEMBER
    )

    account = Account(user_id=user_id, group_id=group_id, role=role.value)
    invite.is_active = not single_use
    session.add(account)
    await session.commit()

    return {"group_id": group_id}


async def delete_group_invites(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> None:
    await check_user_exists(session=session, user_id=user_id)
    _ = await get_group_if_exists(session=session, group_id=group_id)
    await check_user_in_group(session=session, group_id=group_id, user_id=user_id)
    await check_admin_permission_in_group(
        session=session, user_id=user_id, group_id=group_id
    )

    await session.execute(delete(GroupInvite).where(GroupInvite.group_id == group_id))
    await session.commit()
