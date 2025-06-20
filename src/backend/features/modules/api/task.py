from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.tasks.schemas import TaskRead
from features.tasks.services import task as service
from features.users.services.auth import get_current_active_auth_user_id

router = APIRouter()


@router.get(
    "/{module_id}/tasks/",
    response_model=list[TaskRead],
    status_code=status.HTTP_200_OK,
)
async def get_tasks_in_module(
    module_id: int,
    is_active: bool | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    return await service.get_tasks_in_module(session, user_id, module_id, is_active)
