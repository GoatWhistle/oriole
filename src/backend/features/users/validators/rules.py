from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from features.users.schemas import UserAuthRead
from features.groups.services.group import get_user_groups


async def validate_activity_and_verification(
    user_from_db: UserAuthRead,
):
    if not user_from_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password",
        )

    if not user_from_db.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    if not user_from_db.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is unverified",
        )


async def validate_user_has_no_groups(
    session: AsyncSession, user_id: int, raise_exception: bool = True
) -> bool:
    groups = await get_user_groups(session=session, user_id=user_id)
    if groups and raise_exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must leave all groups before deletion",
        )
    return not groups
