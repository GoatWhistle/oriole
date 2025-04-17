from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
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
    get_current_active_auth_user,
)

router = APIRouter(
    prefix=settings.api.v1.auth,
)


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


@router.post("/login")
async def login_user(
    user_data: UserLogin = Depends(validate_registered_user),
    db: AsyncSession = Depends(db_helper.dependency_session_getter),
) -> AccessToken:
    return await crud.login_user(db, user_data)


# @router.get("/users/me")
# async def auth_user_get_self_info(
#     user_data: UserLogin,
# ):
#     return {
#         "id": user_data.id,
#         "email": user_data.email,
#     }
