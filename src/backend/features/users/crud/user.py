from sqlalchemy.ext.asyncio import AsyncSession

from features.users.models import User


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    return await session.get(User, user_id)
