from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import features.groups.crud.account as account_crud
import features.groups.crud.group as group_crud
import features.groups.crud.invite as invite_crud
from features.groups.models import Group, GroupInvite, Account


async def get_group_if_exists(
    session: AsyncSession,
    group_id: int,
) -> Group:
    group = await group_crud.get_group_by_id(session, group_id)

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group {group_id} does not exist",
        )
    return group


async def get_account_if_exists(
    session: AsyncSession,
    user_id: int,
    group_id: int,
    is_correct: bool = True,
) -> Account:
    account = await account_crud.get_account_by_user_id_and_group_id(
        session, user_id, group_id
    )

    if not account and is_correct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {user_id} do not have account in group {group_id}.",
        )
    elif account and not is_correct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {user_id} is already have account in group {group_id}.",
        )
    return account


async def get_group_invite_if_exists(
    session: AsyncSession,
    code: str,
) -> GroupInvite:
    group_invite = await invite_crud.get_group_invite_by_code(session, code)

    if not group_invite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group invite code {code} does not exist",
        )
    return group_invite
