from sqlalchemy.ext.asyncio import AsyncSession

import features.accounts.crud.account as account_crud
import features.groups.crud.group as group_crud
import features.groups.crud.invite as invite_crud
from features.accounts.models import Account
from features.groups.exceptions import (
    AccountNotFoundInSpaceException,
    GroupNotFoundException,
    GroupInviteNotFoundException,
    AccountAlreadyInSpaceException,
)
from features.groups.models import Group, GroupInvite


async def get_group_or_404(
    session: AsyncSession,
    group_id: int,
) -> Group:
    group = await group_crud.get_group_by_id(session, group_id)
    if not group:
        raise GroupNotFoundException()
    return group


async def get_account_or_404(
    session: AsyncSession,
    user_id: int,
    space_id: int,
    is_correct: bool = True,
) -> Account:
    account = await account_crud.get_account_by_user_id_and_space_id(
        session, user_id, space_id
    )

    if not account and is_correct:
        raise AccountNotFoundInSpaceException()
    elif account and not is_correct:
        raise AccountAlreadyInSpaceException()
    return account


async def get_group_invite_or_404(
    session: AsyncSession,
    code: str,
) -> GroupInvite:
    group_invite = await invite_crud.get_group_invite_by_code(session, code)
    if not group_invite:
        raise GroupInviteNotFoundException()
    return group_invite
