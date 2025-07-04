from sqlalchemy.ext.asyncio import AsyncSession

from features.spaces.models import Space


async def get_space_by_id(
    session: AsyncSession,
    space_id: int,
) -> Space | None:
    return await session.get(Space, space_id)
