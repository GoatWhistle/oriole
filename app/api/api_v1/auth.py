from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.token import AccessToken
from core.models import db_helper
from crud import auth as crud

from core.schemas.user import (
    RegisterUser,
    UserAuthRead,
    UserLogin,
)
from crud.auth import (
    validate_registered_user,
)

router = APIRouter()


@router.post(
    "/register",
    response_model=UserAuthRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: RegisterUser,
    db: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    return await crud.register_user(db, user_data)


@router.post(
    "/token",
    response_model=AccessToken,
    status_code=status.HTTP_201_CREATED,
)
async def login_for_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    try:
        user_data = UserLogin(email=form_data.username, password=form_data.password)

        await validate_registered_user(user_data, db)

        return await crud.login_user(db, user_data)
    except HTTPException as e:
        raise e
