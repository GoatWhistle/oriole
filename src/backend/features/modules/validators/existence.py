from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from features.modules.models import Module


async def get_module_if_exists(
    session: AsyncSession,
    module_id: int | Mapped[int],
) -> Module | Type[Module]:
    module = await session.get(Module, module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module {module_id} does not exist",
        )
    return module
