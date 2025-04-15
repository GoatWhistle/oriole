from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from core.config import settings
from core.models import db_helper
from crud import auth as crud

from core.schemas.user import (
    UserCreate,
)

router = APIRouter(
    prefix=settings.api.v1.auth,
)


@router.post(
    "/register",
    response_model=UserCreate,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    return await crud.register_user(db, user_data)
