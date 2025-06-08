from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from tasks.schemas import TaskRead
from tasks.services import copy as service
from users.services.auth import get_current_active_auth_user_id

router = APIRouter()

@router.post(
    "/{task_id}/copy-to-module/{target_module_id}",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
async def copy_task_to_module(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    task_id: int,
    target_module_id: int,
):
    return await service.copy_task_to_module(
        session=session,
        user_id=user_id,
        source_task_id=task_id,
        target_module_id=target_module_id,
    )
