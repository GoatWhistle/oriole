from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.groups.services import module as service
from features.modules.schemas import ModuleReadPartial
from features.users.services.auth import get_current_active_auth_user_id

router = APIRouter()


@router.get(
    "/{group_id}/modules/",
    response_model=Sequence[ModuleReadPartial],
    status_code=status.HTTP_200_OK,
)
async def get_modules_in_group(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    group_id: int,
):
    return await service.get_modules_in_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
    )
