from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.modules.schemas import ModuleRead
from features.modules.services import copy as service
from features.users.services.auth import get_current_active_auth_user_id

router = APIRouter()

@router.post(
    "/{module_id}/copy-to-group/{target_group_id}",
    response_model=ModuleRead,
    status_code=status.HTTP_201_CREATED,
)
async def copy_module(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    module_id: int,
    target_group_id: int,
):
    return await service.copy_module_to_group(
        session=session,
        user_id=user_id,
        module_id=module_id,
        target_group_id=target_group_id,
    )