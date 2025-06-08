from typing import Annotated, Sequence, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from modules.services import task as service
from tasks.schemas import TaskReadPartial
from users.services.auth import get_current_active_auth_user_id

router = APIRouter()


@router.get(
    "/{module_id}/tasks/",
    response_model=Sequence[TaskReadPartial],
    status_code=status.HTTP_200_OK,
)
async def get_tasks_in_module(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    module_id: int,
    is_correct: Optional[bool] = None,
) -> Sequence[TaskReadPartial]:
    return await service.get_tasks_in_module(
        session=session,
        user_id=user_id,
        module_id=module_id,
        is_correct=is_correct,
    )