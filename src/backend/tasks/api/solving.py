from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from tasks.schemas import TaskRead
from tasks.services import solving as service
from users.crud.auth import get_current_active_auth_user_id

router = APIRouter()


@router.patch(
    "/{task_id}/complete/",
    response_model=TaskRead,
    status_code=status.HTTP_200_OK,
)
async def try_to_complete_task(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    task_id: int,
    user_answer: str,
):
    return await service.try_to_complete_task(
        session=session,
        user_id=user_id,
        task_id=task_id,
        user_answer=user_answer,
    )

