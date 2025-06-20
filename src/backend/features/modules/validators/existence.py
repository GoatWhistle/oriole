from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import features.modules.crud.module as module_crud
from features.modules.models import Module


async def get_module_if_exists(
    session: AsyncSession,
    module_id: int,
) -> Module:
    module = await module_crud.get_module_by_id(session, module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module {module_id} does not exist",
        )
    return module
