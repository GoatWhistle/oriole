from typing import Any

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from database import DbHelper
from features.modules.models import Module
from features.modules.schemas import ModuleCreate
from utils import get_current_utc


async def create_module(
    session: AsyncSession,
    module_data: ModuleCreate,
    user_id: int,
) -> Module:
    is_active = (
        module_data.start_datetime <= get_current_utc() <= module_data.end_datetime
    )
    module = Module(
        **module_data.model_dump(exclude={"is_active"}),
        is_active=is_active,
    )
    module.creator_id = user_id
    session.add(module)
    await session.commit()
    await session.refresh(module)
    return module


async def get_module_by_id(
    session: AsyncSession,
    module_id: int,
) -> Module | None:
    return await session.get(Module, module_id)


async def get_modules(
    session: AsyncSession,
    is_active: bool | None = None,
) -> list[Module]:
    statement = select(Module)
    if is_active is not None:
        statement = statement.where(Module.is_active == is_active)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_modules_by_group_id(
    session: AsyncSession,
    space_id: int,
    is_active: bool | None = None,
) -> list[Module]:
    return await get_modules_by_space_ids(session, [space_id], is_active)


async def get_modules_by_space_ids(
    session: AsyncSession,
    space_ids: list[int],
    is_active: bool | None = None,
) -> list[Module]:
    statement = select(Module).where(Module.space_id.in_(space_ids))
    if is_active is not None:
        statement = statement.where(Module.is_active == is_active)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def update_module(
    session: AsyncSession,
    module: Module,
    update_data: dict[str, Any],
) -> Module:
    for key, value in update_data.items():
        setattr(module, key, value)
    await session.commit()
    await session.refresh(module)
    return module


async def update_modules_activity():
    local_db_helper = DbHelper(url=str(settings.db.url))

    async with local_db_helper.session_factory() as session:
        modules = await get_modules(session)

        updated = False
        for module in modules:
            new_status = (
                module.start_datetime <= get_current_utc() <= module.end_datetime
            )
            if module.is_active != new_status:
                module.is_active = new_status
                updated = True

        if updated:
            await session.commit()

        await local_db_helper.dispose()


async def increment_module_tasks_count(
    session: AsyncSession,
    module_id: int,
) -> None:
    await session.execute(
        update(Module)
        .where(Module.id == module_id)
        .values(tasks_count=Module.tasks_count + 1)
    )
    await session.commit()


async def delete_module(
    session: AsyncSession,
    module: Module,
) -> None:
    await session.delete(module)
    await session.commit()
