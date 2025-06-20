from typing import Sequence

from sqlalchemy import select, delete, Result
from sqlalchemy.ext.asyncio import AsyncSession

from features.groups.models import Account
from features.groups.schemas import AccountRole
from features.tasks.models import UserReply


async def create_account(
    session: AsyncSession,
    user_id: int,
    group_id: int,
    role: int,
) -> Account:
    account = Account(user_id=user_id, group_id=group_id, role=role)
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account


async def get_accounts_by_group_id(
    session: AsyncSession,
    group_id: int,
) -> Sequence[Account]:
    result = await session.execute(select(Account).where(Account.group_id == group_id))
    return result.scalars().all()


async def get_account_by_user_id_and_group_id(
    session: AsyncSession,
    user_id: int,
    group_id: int,
) -> Account | None:
    statement = select(Account).where(
        Account.user_id == user_id, Account.group_id == group_id
    )
    result: Result = await session.execute(statement)
    return result.scalars().first()


async def get_admins_accounts_by_group(
    session: AsyncSession,
    group_id: int,
) -> Sequence[Account]:
    statement = select(Account).where(
        Account.group_id == group_id,
        Account.role == AccountRole.ADMIN.value,
    )
    result: Result = await session.execute(statement)
    return result.scalars().all()


async def get_members_accounts_by_group(
    session: AsyncSession,
    group_id: int,
) -> Sequence[Account]:
    statement = select(Account).where(
        Account.group_id == group_id,
        Account.role == AccountRole.MEMBER.value,
    )
    result: Result = await session.execute(statement)
    return result.scalars().all()


async def get_accounts_by_user_id(
    session: AsyncSession, user_id: int
) -> Sequence[Account]:
    result = await session.execute(select(Account).where(Account.user_id == user_id))
    return result.scalars().all()


async def get_accounts_in_group(
    session: AsyncSession,
    group_id: int,
) -> Sequence[Account]:
    result = await session.execute(select(Account).where(Account.group_id == group_id))
    return result.scalars().all()


async def update_account_role(
    session: AsyncSession,
    account: Account,
    new_role: int,
) -> None:
    account.role = new_role
    await session.commit()


async def delete_user_replies_by_account_id(
    session: AsyncSession,
    account_id: int,
) -> None:
    await session.execute(delete(UserReply).where(UserReply.account_id == account_id))


async def delete_account(
    session: AsyncSession,
    account: Account,
) -> None:
    await session.delete(account)


async def delete_accounts_by_group_id(
    session: AsyncSession,
    group_id: int,
) -> None:
    await session.execute(delete(Account).where(Account.group_id == group_id))
