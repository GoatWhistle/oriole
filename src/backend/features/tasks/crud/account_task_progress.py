from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from features.tasks.models import AccountTaskProgress


async def create_account_task_progress(
    session: AsyncSession,
    account_id: int,
    task_id: int,
    is_correct: bool,
    user_attempts_count: int,
) -> AccountTaskProgress:
    account_task_progress = AccountTaskProgress(
        account_id=account_id,
        task_id=task_id,
        is_correct=is_correct,
        user_attempts_count=user_attempts_count,
    )
    session.add(account_task_progress)
    await session.commit()
    await session.refresh(account_task_progress)
    return account_task_progress


async def get_account_task_progresses(
    session: AsyncSession,
    account_ids: list[int] | None = None,
    task_ids: list[int] | None = None,
) -> list[AccountTaskProgress]:
    statement = select(AccountTaskProgress)
    conditions = []

    if account_ids is not None:
        conditions.append(AccountTaskProgress.account_id.in_(account_ids))
    if task_ids is not None:
        conditions.append(AccountTaskProgress.task_id.in_(task_ids))

    if conditions:
        statement = statement.where(*conditions)

    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_account_task_progresses_by_account_ids_and_task_ids(
    session: AsyncSession,
    account_ids: list[int],
    task_ids: list[int],
) -> list[AccountTaskProgress]:
    return await get_account_task_progresses(session, account_ids, task_ids)


async def get_account_task_progresses_by_account_id_and_task_ids(
    session: AsyncSession,
    account_id: int,
    task_ids: list[int],
) -> list[AccountTaskProgress]:
    return await get_account_task_progresses(session, [account_id], task_ids)


async def get_account_task_progress_by_account_id_and_task_id(
    session: AsyncSession,
    account_id: int,
    task_id: int,
) -> AccountTaskProgress | None:
    result = await get_account_task_progresses(session, [account_id], [task_id])
    return result[0] if result else None


async def increment_user_attempts_count(
    session: AsyncSession,
    account_task_progress: AccountTaskProgress,
) -> None:
    account_task_progress.user_attempts_count += 1
    await session.commit()
    await session.refresh(account_task_progress)


async def change_is_correct_status(
    session: AsyncSession,
    account_task_progress: AccountTaskProgress,
    is_correct: bool,
) -> None:
    account_task_progress.is_correct = is_correct
    await session.commit()
    await session.refresh(account_task_progress)


async def delete_account_task_progresses_by_task_id(
    session: AsyncSession,
    task_id: int,
) -> None:
    await session.execute(
        delete(AccountTaskProgress).where(AccountTaskProgress.task_id == task_id)
    )
    await session.commit()
