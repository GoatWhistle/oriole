from secrets import choice
from string import ascii_uppercase, digits
from urllib.parse import urljoin

from fastapi import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import features.groups.crud.account as account_crud
import features.groups.crud.invite as group_invite_crud
from features.groups.models import GroupInvite
from features.groups.schemas import AccountRole
from features.groups.validators import (
    get_group_or_404,
    get_account_or_404,
    check_user_is_admin_or_owner,
    get_group_invite_or_404,
    check_group_invite_active,
    check_group_invite_not_expired,
)
from features.users.validators import check_user_exists


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
):
    await check_user_exists(session, user_id)

    _ = await get_group_or_404(session, group_id)
    account = await get_account_or_404(session, user_id, group_id)

    check_user_is_admin_or_owner(account.role)

    code = await generate_unique_group_invite_code(session)
    code += "1" if single_use else "0"

    await group_invite_crud.create_group_invite(
        session, group_id, code, expires_minutes
    )

    base_url = str(request.base_url).rstrip("/")
    return {"link": urljoin(base_url, f"/groups/join/{code}")}


async def join_by_link(
    session: AsyncSession,
    user_id: int,
    invite_code: str,
) -> dict:

    await check_user_exists(session, user_id)

    single_use = invite_code[-1] == "1"
    invite = await get_group_invite_or_404(session, invite_code)
    check_group_invite_active(invite.is_active)
    check_group_invite_not_expired(invite.expires_at)
    group_id = invite.group_id

    await get_account_or_404(session, user_id, group_id, is_correct=False)

    accounts = await account_crud.get_accounts_in_group(session, group_id)
    role = AccountRole.OWNER if not accounts else AccountRole.MEMBER

    await account_crud.create_account(session, user_id, group_id, role.value)

    if single_use:
        await group_invite_crud.set_invite_inactive(session, invite)

    return {"group_id": group_id}


async def delete_group_invites(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> None:
    await check_user_exists(session, user_id)

    _ = await get_group_or_404(session, group_id)
    account = await get_account_or_404(session, group_id, user_id)

    check_user_is_admin_or_owner(account.role)

    await group_invite_crud.delete_group_invites_by_group_id(session, group_id)
