from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
    Request,
)
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr, Field
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.users.schemas.token import TokenResponseForOAuth2
from features.users.schemas.user import (
    RegisterUserInput,
    UserAuthRead,
    UserRead,
)
from features.users.services import auth as service

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/register",
    response_model=UserAuthRead,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("10/hour")
async def register_user(
    request: Request,
    user_data: RegisterUserInput,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    return await service.register_user(
        request=request,
        session=session,
        user_data=user_data,
    )


@router.post(
    "/token",
    response_model=TokenResponseForOAuth2,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
async def login_for_token(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    _ = request
    return await service.login_for_token(
        session=session,
        form_data=form_data,
        response=response,
    )


@router.delete(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(
    request: Request,
    response: Response,
):
    return await service.logout(
        request=request,
        response=response,
    )


@router.put("/refresh")
async def refresh_tokens(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    return await service.refresh_tokens(
        request=request,
        response=response,
        session=session,
    )


@router.get(
    "/check-auth",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def check_auth(
    payload: dict = Depends(service.get_non_expire_payload_token),
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    return await service.check_auth(
        session=session,
        payload=payload,
    )


@router.post("/reset_password")
@limiter.limit("3/minute")
async def reset_password(
    request: Request,
    user_from_db: UserAuthRead = Depends(service.get_current_auth_user),
):
    return await service.reset_password(
        user_from_db=user_from_db,
        request=request,
    )


@router.post("/forgot_password")
@limiter.limit("3/minute")
async def forgot_password(
    email: Annotated[EmailStr, Field(max_length=63)],
    request: Request,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    return await service.forgot_password(
        request=request,
        email=email,
        session=session,
    )


@router.post("/send_email_again")
@limiter.limit("3/minute")
async def send_confirmation_email_again(
    request: Request,
    user_data: UserAuthRead = Depends(service.get_current_auth_user),
):
    return await service.send_confirmation_email_again(
        request=request,
        user_data=user_data,
    )
