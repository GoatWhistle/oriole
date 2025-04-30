from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
)

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.token import TokenResponseForOAuth2
from core.models import db_helper
from crud import auth as crud

from core.schemas.user import (
    RegisterUser,
    UserAuthRead,
)


router = APIRouter()


@router.post(
    "/register",
    response_model=UserAuthRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: RegisterUser,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    return await crud.register_user(session, user_data)


@router.post(
    "/token",
    response_model=TokenResponseForOAuth2,
    status_code=status.HTTP_201_CREATED,
)
async def login_for_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    return await crud.login_for_token(
        session=session,
        form_data=form_data,
        response=response,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(response: Response):
    response.delete_cookie("access_token")
