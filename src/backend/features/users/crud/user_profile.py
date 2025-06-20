from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from features.users.models import UserProfile


async def get_user_profiles_by_user_ids(
    session: AsyncSession, user_ids: Sequence[int]
) -> Sequence[UserProfile]:
    if not user_ids:
        return []
    result = await session.execute(
        select(UserProfile).where(UserProfile.user_id.in_(user_ids))
    )
    return result.scalars().all()
