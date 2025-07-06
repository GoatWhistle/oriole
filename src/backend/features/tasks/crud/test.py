from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from features.tasks.models import Test
from features.tasks.schemas import TestCreate


async def create_test(
    session: AsyncSession,
    test_in: TestCreate,
) -> Test:
    test = Test(
        **test_in.model_dump(),
    )
    session.add(test)
    await session.commit()
    await session.refresh(test)
    return test


async def update_test(
    session: AsyncSession,
    test: Test,
    test_update: dict[str, Any],
) -> Test:
    for key, value in test_update.items():
        setattr(test, key, value)
    await session.commit()
    await session.refresh(test)
    return test


async def get_tests_by_task_id(
    session: AsyncSession,
    task_id: int,
) -> list[Test]:
    stmt = select(Test).where(Test.task_id == task_id)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_test_by_id(
    session: AsyncSession,
    test_id: int,
) -> Test:
    stmt = select(Test).where(Test.id == test_id)
    result = await session.execute(stmt)
    return result.scalar()


async def delete_test(
    session: AsyncSession,
    test: Test,
) -> None:
    await session.delete(test)
    await session.commit()
