from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import features.users.crud.user as user_crud
import features.users.crud.user_profile as user_profile_crud
from features import UserProfile


async def check_user_exists(
    session: AsyncSession,
    user_id: int,
) -> None:
    user = await user_crud.get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} does not exist",
        )


async def get_user_profile_if_exists(
    session: AsyncSession,
    user_id: int,
) -> UserProfile:
    profile = await user_profile_crud.get_user_profile_by_user_id(session, user_id)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"UserProfile for user {user_id} does not exist",
        )
    return profile
