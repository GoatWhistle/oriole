from fastapi import APIRouter, Depends, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.user import (
    UserProfileRead,
    UserProfileUpdate,
    UserProfileUpdatePartial,
    EmailUpdateRead,
    EmailUpdate,
)

from crud import users as crud
from crud.auth import get_current_active_auth_user_id

router = APIRouter()


@router.put("/{user_id}/profile", response_model=UserProfileRead)
async def update_user(
    user_data: UserProfileUpdate | UserProfileUpdatePartial,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    return await crud.update_user_profile(
        session=session,
        user_data=user_data,
        user_id=user_id,
    )


@router.patch("/{user_id}/profile", response_model=UserProfileRead)
async def update_user_partial(
    user_data: UserProfileUpdatePartial,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    return await crud.update_user_profile(
        session=session,
        user_data=user_data,
        user_id=user_id,
        partial=True,
    )


@router.put("/{user_id}/email", response_model=EmailUpdateRead)
async def update_user_email(
    response: Response,
    request: Request,
    user_data: EmailUpdate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    return await crud.update_user_email(
        session=session,
        user_data=user_data,
        user_id=user_id,
        request=request,
        response=response,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    response: Response,
    request: Request,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    return await crud.delete_user(
        session=session,
        user_id=user_id,
        request=request,
        response=response,
    )
