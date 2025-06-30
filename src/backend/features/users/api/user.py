from fastapi import APIRouter, Depends, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.users.schemas.user import (
    UserProfileRead,
    UserProfileUpdate,
    UserProfileUpdatePartial,
    EmailChangeRequest,
)
from features.users.services import user as service
from features.users.services.auth import get_current_active_auth_user_id

router = APIRouter()


@router.put("/profile", response_model=UserProfileRead)
async def update_user(
    user_data: UserProfileUpdate | UserProfileUpdatePartial,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    return await service.update_user_profile(
        session=session,
        user_data=user_data,
        user_id=user_id,
    )


@router.patch("/profile", response_model=UserProfileRead)
async def update_user_partial(
    user_data: UserProfileUpdatePartial,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    return await service.update_user_profile(
        session=session,
        user_data=user_data,
        user_id=user_id,
        partial=True,
    )


@router.post("/change_email")
async def change_user_email(
    request: Request,
    data: EmailChangeRequest,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    return await service.change_user_email(
        request=request,
        email=data.current_email,
        new_email=data.new_email,
        session=session,
    )


@router.get("/get-role/group/{group_id}")
async def get_int_role_in_group(
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
) -> int:
    return await service.get_int_role_in_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    response: Response,
    request: Request,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    return await service.delete_user(
        session=session,
        user_id=user_id,
        request=request,
        response=response,
    )
