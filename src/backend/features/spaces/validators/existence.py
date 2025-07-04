from sqlalchemy.ext.asyncio import AsyncSession

import features.spaces.crud.space as space_crud
from features.spaces.exceptions import SpaceNotFoundException
from features.spaces.models import Space


async def get_space_or_404(
    session: AsyncSession,
    space_id: int,
) -> Space:
    group = await space_crud.get_space_by_id(session, space_id)
    if not group:
        raise SpaceNotFoundException()
    return group
