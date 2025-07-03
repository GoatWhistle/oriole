from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from features.accounts.models import Account
from features.solutions.models import BaseSolution


async def create_account(
    session: AsyncSession,
    user_id: int,
    space_id: int,
    role: int,
) -> Account:
    account = Account(
        user_id=user_id,
        space_id=space_id,
        role=role,
    )
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account


async def get_accounts_by_space_id(
    session: AsyncSession,
    space_id: int,
) -> list[Account]:
    result = await session.execute(select(Account).where(Account.space_id == space_id))
    return list(result.scalars().all())


async def get_accounts_in_spaces(
    session: AsyncSession,
    group_ids: list[int],
) -> list[Account]:
    if not group_ids:
        return []
    statement = select(Account).where(Account.space_id.in_(group_ids))
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_account_by_user_id_and_space_id(
    session: AsyncSession,
    user_id: int,
    space_id: int,
) -> Account | None:
    statement = select(Account).where(
        Account.user_id == user_id, Account.space_id == space_id
    )
    result = await session.execute(statement)
    return result.scalars().first()


async def get_accounts_by_space_and_role(
    session: AsyncSession,
    space_id: int,
    role: int,
) -> list[Account]:
    statement = select(Account).where(
        Account.space_id == space_id,
        Account.role == role,
    )
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_accounts_by_user_id(session: AsyncSession, user_id: int) -> list[Account]:
    result = await session.execute(select(Account).where(Account.user_id == user_id))
    return list(result.scalars().all())


async def get_accounts_in_space(
    session: AsyncSession,
    space_id: int,
) -> list[Account]:
    result = await session.execute(select(Account).where(Account.space_id == space_id))
    return list(result.scalars().all())


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
    await session.execute(
        delete(BaseSolution).where(BaseSolution.account_id == account_id)
    )


async def delete_account(
    session: AsyncSession,
    account: Account,
) -> None:
    await session.delete(account)


async def delete_accounts_by_group_id(
    session: AsyncSession,
    space_id: int,
) -> None:
    await session.execute(delete(Account).where(Account.space_id == space_id))
