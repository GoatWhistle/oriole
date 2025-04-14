from fastapi import HTTPException, status
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Account, Group, User
from core.schemas.account import AccountRole


async def check_group_exists(
    session: AsyncSession,
    group_id: int,
) -> None:
    group = await session.get(Group, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group {group_id} not found",
        )


async def check_admin_permission(
    user_id: int,
    group: Group,
) -> None:
    admin_accounts = [
        account
        for account in group.accounts
        if account.role == AccountRole.TEACHER.value
    ]
    if not any(account.user_id == user_id for account in admin_accounts):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} does not have permission to perform this action in group {group.id}.",
        )


async def check_user_in_group(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> None:

    statement = select(Account).where(
        Account.user_id == user_id, Account.group_id == group_id
    )
    result = await session.execute(statement)
    account = result.scalars().first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} is not a member of this group {group_id}.",
        )
