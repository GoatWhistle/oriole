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
from features.users.services import auth as crud

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/register",
    response_model=UserAuthRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    request: Request,
    user_data: RegisterUserInput,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    return await crud.register_user(
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
    return await crud.login_for_token(
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
    return await crud.logout(
        request=request,
        response=response,
    )


@router.put("/refresh")
async def refresh_tokens(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    return await crud.refresh_tokens(
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
    payload: dict = Depends(crud.get_non_expire_payload_token),
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    return await crud.check_auth(
        session=session,
        payload=payload,
    )


@router.post("/reset_password")
async def reset_password(
    user_from_db: UserAuthRead = Depends(crud.get_current_auth_user),
):
    return await crud.reset_password(
        user_from_db=user_from_db,
    )


@router.post("/forgot_password")
@limiter.limit("5/minute")
async def forgot_password(
    email: Annotated[EmailStr, Field(max_length=63)],
    request: Request,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    _ = request
    return await crud.forgot_password(
        email=email,
        session=session,
    )


@router.post("/send_email_again")
async def send_confirmation_email_again(
    user_data: UserAuthRead = Depends(crud.get_current_auth_user),
):
    return await crud.send_confirmation_email_again(user_data=user_data)
