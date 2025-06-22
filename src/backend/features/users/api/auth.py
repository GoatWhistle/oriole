from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
    Request,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr, Field
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.users.schemas.token import TokenResponseForOAuth2, SuccessAuthAction
from features.users.schemas.user import (
    RegisterUserInput,
    UserAuthRead,
    UserRead,
)
from features.users.services import auth as service
from utils import get_current_utc
from utils.schemas import SuccessResponse, Meta

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/register",
    response_model=SuccessResponse[UserAuthRead],
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("10/hour")
async def register_user(
    request: Request,
    user_data: RegisterUserInput,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    data = await service.register_user(
        request=request,
        session=session,
        user_data=user_data,
    )
    response_content = jsonable_encoder(
        SuccessResponse[UserAuthRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=201)


@router.post(
    "/token",
    response_model=SuccessResponse[TokenResponseForOAuth2],
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
    data = await service.login_for_token(
        session=session,
        form_data=form_data,
        response=response,
    )
    response_content = jsonable_encoder(
        SuccessResponse[TokenResponseForOAuth2](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=201)


@router.delete(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=SuccessResponse[SuccessAuthAction],
)
async def logout(
    request: Request,
    response: Response,
):
    data = await service.logout(
        request=request,
        response=response,
    )
    response_content = jsonable_encoder(
        SuccessResponse[SuccessAuthAction](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=201)


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
    response_model=SuccessResponse[UserRead],
    status_code=status.HTTP_200_OK,
)
async def check_auth(
    payload: dict = Depends(service.get_non_expire_payload_token),
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    data = await service.check_auth(
        session=session,
        payload=payload,
    )
    response_content = jsonable_encoder(
        SuccessResponse[UserRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=201)


@router.post("/reset_password", response_model=SuccessResponse[SuccessAuthAction])
@limiter.limit("3/minute")
async def reset_password(
    request: Request,
    user_from_db: UserAuthRead = Depends(service.get_current_auth_user),
):
    data = await service.reset_password(
        user_from_db=user_from_db,
        request=request,
    )
    response_content = jsonable_encoder(
        SuccessResponse[SuccessAuthAction](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=201)


@router.post("/forgot_password", response_model=SuccessResponse[SuccessAuthAction])
@limiter.limit("3/minute")
async def forgot_password(
    email: Annotated[EmailStr, Field(max_length=63)],
    request: Request,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    data = await service.forgot_password(
        request=request,
        email=email,
        session=session,
    )
    response_content = jsonable_encoder(
        SuccessResponse[SuccessAuthAction](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=201)


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
