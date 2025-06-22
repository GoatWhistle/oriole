from sqlalchemy.ext.asyncio import AsyncSession

import features.modules.crud.module as module_crud
from features.modules.exceptions import ModuleNotFoundException
from features.modules.models import Module


async def get_module_or_404(
    session: AsyncSession,
    module_id: int,
) -> Module:
    module = await module_crud.get_module_by_id(session, module_id)
    if not module:
        raise ModuleNotFoundException()
    return module
