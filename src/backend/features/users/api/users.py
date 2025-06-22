from fastapi import APIRouter, Depends, status, Response, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.users.schemas.user import (
    UserProfileRead,
    UserProfileUpdate,
    UserProfileUpdatePartial,
    EmailUpdateRead,
    EmailUpdate,
    UserRole,
)
from features.users.services import user as crud
from features.users.services.auth import get_current_active_auth_user_id
from utils import get_current_utc
from utils.schemas import SuccessResponse, Meta

router = APIRouter()


@router.put("/profile", response_model=SuccessResponse[UserProfileRead])
async def update_user(
    user_data: UserProfileUpdate | UserProfileUpdatePartial,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await crud.update_user_profile(
        session=session,
        user_data=user_data,
        user_id=user_id,
    )
    response_content = jsonable_encoder(
        SuccessResponse[UserProfileRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=200)


@router.patch("/profile", response_model=SuccessResponse[UserProfileRead])
async def update_user_partial(
    user_data: UserProfileUpdatePartial,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await crud.update_user_profile(
        session=session,
        user_data=user_data,
        user_id=user_id,
        partial=True,
    )
    response_content = jsonable_encoder(
        SuccessResponse[UserProfileRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=200)


@router.put("/email", response_model=SuccessResponse[EmailUpdateRead])
async def update_user_email(
    response: Response,
    request: Request,
    user_data: EmailUpdate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await crud.update_user_email(
        session=session,
        user_data=user_data,
        user_id=user_id,
        request=request,
        response=response,
    )
    response_content = jsonable_encoder(
        SuccessResponse[EmailUpdateRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=200)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
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


@router.get(
    "/get-role/group/{group_id}",
    response_model=SuccessResponse[UserRole],
)
async def get_int_role_in_group(
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await crud.get_int_role_in_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )
    response_content = jsonable_encoder(
        SuccessResponse[UserRole](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=200)
