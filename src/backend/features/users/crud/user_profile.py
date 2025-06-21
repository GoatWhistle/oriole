from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from features.users.models import UserProfile


async def get_user_profile_by_user_id(
    session: AsyncSession,
    user_id: int,
) -> UserProfile | None:
    return await session.get(UserProfile, user_id)


async def get_user_profiles_by_user_ids(
    session: AsyncSession,
    user_ids: list[int],
) -> list[UserProfile]:
    if not user_ids:
        return []
    result = await session.execute(
        select(UserProfile).where(UserProfile.user_id.in_(user_ids))
    )
    return list(result.scalars().all())
