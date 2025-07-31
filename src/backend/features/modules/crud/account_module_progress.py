from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from features.modules.models import AccountModuleProgress


async def create_account_module_progress(
    session: AsyncSession,
    account_id: int,
    module_id: int,
    user_completed_tasks_count: int,
) -> AccountModuleProgress:
    account_module_progress = AccountModuleProgress(
        account_id=account_id,
        module_id=module_id,
        user_completed_tasks_count=user_completed_tasks_count,
    )
    session.add(account_module_progress)
    await session.commit()
    await session.refresh(account_module_progress)
    return account_module_progress


async def get_account_module_progresses(
    session: AsyncSession,
    account_ids: list[int] | None = None,
    module_ids: list[int] | None = None,
) -> list[AccountModuleProgress]:
    statement = select(AccountModuleProgress)
    conditions = []

    if account_ids is not None:
        conditions.append(AccountModuleProgress.account_id.in_(account_ids))
    if module_ids is not None:
        conditions.append(AccountModuleProgress.module_id.in_(module_ids))

    if conditions:
        statement = statement.where(*conditions)

    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_account_module_progresses_by_account_ids_and_module_ids(
    session: AsyncSession,
    account_ids: list[int],
    module_ids: list[int],
) -> list[AccountModuleProgress]:
    return await get_account_module_progresses(session, account_ids, module_ids)


async def get_account_module_progresses_by_account_id_and_module_ids(
    session: AsyncSession,
    account_id: int,
    module_ids: list[int],
) -> list[AccountModuleProgress]:
    return await get_account_module_progresses(session, [account_id], module_ids)


async def get_account_module_progress_by_account_id_and_module_id(
    session: AsyncSession,
    account_id: int,
    module_id: int,
) -> AccountModuleProgress | None:
    result = await get_account_module_progresses(session, [account_id], [module_id])
    return result[0] if result else None


async def increment_user_completed_tasks_count(
    session: AsyncSession,
    account_module_progress: AccountModuleProgress,
) -> None:
    account_module_progress.user_completed_tasks_count += 1
    await session.commit()
    await session.refresh(account_module_progress)


async def delete_account_module_progresses_by_module_id(
    session: AsyncSession,
    module_id: int,
) -> None:
    await session.execute(
        delete(AccountModuleProgress).where(
            AccountModuleProgress.module_id == module_id
        )
    )
    await session.commit()
