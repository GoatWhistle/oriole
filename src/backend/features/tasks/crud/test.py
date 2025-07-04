from typing import Any

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


async def get_tests(
    session,
    task_id,
):
    pass
