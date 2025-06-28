from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from features.users.models import UserProfile
from features.users.schemas import RegisterUserInput


async def get_user_profile_by_id(
    session: AsyncSession,
    profile_id: int,
) -> UserProfile | None:
    statement = select(UserProfile).filter_by(user_id=profile_id)
    profile_from_db = await session.scalars(statement)
    profile_from_db = profile_from_db.first()

    return profile_from_db


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


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    profile_data: RegisterUserInput,
) -> UserProfile:
    profile = UserProfile(
        user_id=user_id,
        name=profile_data.name,
        surname=profile_data.surname,
        patronymic=profile_data.patronymic,
    )
    session.add(profile)
    await session.commit()
    return profile


async def update_profile(
    session: AsyncSession,
    profile: UserProfile,
    update_data: dict,
) -> UserProfile:
    for field, value in update_data.items():
        if hasattr(profile, field):
            setattr(profile, field, value)

    await session.commit()
    await session.refresh(profile)
    return profile
