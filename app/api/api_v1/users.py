from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.user import (
    UserRead,
    UserUpdate,
    UserUpdatePartial,
)

from crud import users as crud
from crud.auth import get_current_active_auth_user_id

router = APIRouter()


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_data: UserUpdate | UserUpdatePartial,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    current_user_id: int = Depends(get_current_active_auth_user_id),
):
    return await crud.update_user(session, user_id, user_data, current_user_id)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user_partial(
    user_id: int,
    user_update: UserUpdatePartial,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    current_user_id: int = Depends(get_current_active_auth_user_id),
):
    return await crud.update_user(
        session, user_id, user_update, current_user_id, partial=True
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    current_user_id: int = Depends(get_current_active_auth_user_id),
):
    await crud.delete_user(session, current_user_id, user_id)
