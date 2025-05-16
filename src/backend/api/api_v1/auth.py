from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
    Request,
)

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.token import TokenResponseForOAuth2
from core.models import db_helper
from crud import auth as crud
from slowapi import Limiter
from slowapi.util import get_remote_address

from core.schemas.user import (
    RegisterUser,
    UserAuthRead,
    UserRead,
)


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/register",
    response_model=UserAuthRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    request: Request,
    user_data: RegisterUser,
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
