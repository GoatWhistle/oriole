from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Sequence

from core.models import db_helper

from core.schemas.task import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
    TaskUpdatePartial,
)

from crud import tasks as crud

from crud.auth import get_current_active_auth_user_id

router = APIRouter()


@router.post(
    "/",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    task_in: TaskCreate,
):
    return await crud.create_task(
        session=session,
        user_id=current_user_id,
        task_in=task_in,
    )


@router.get(
    "/{task_id}/",
    response_model=TaskRead,
)
async def get_task(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    task_id: int,
):
    return await crud.get_task(
        session=session,
        user_id=current_user_id,
        task_id=task_id,
    )


@router.get(
    "/",
    response_model=Sequence[TaskRead],
)
async def get_tasks(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    assignment_id: int,
):
    return await crud.get_tasks(
        session=session,
        user_id=current_user_id,
        assignment_id=assignment_id,
    )


@router.put("/{task_id}/")
async def update_task(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    task_update: TaskUpdate,
    task_id: int,
):
    return await crud.update_task(
        session=session,
        user_id=current_user_id,
        task_id=task_id,
        task_update=task_update,
    )


@router.patch("/{task_id}/")
async def update_task_partial(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    task_update: TaskUpdatePartial,
    task_id: int,
):
    return await crud.update_task(
        session=session,
        user_id=current_user_id,
        task_id=task_id,
        task_update=task_update,
        partial=True,
    )


@router.delete(
    "/{task_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    task_id: int,
) -> None:
    await crud.delete_task(
        session=session,
        user_id=current_user_id,
        task_id=task_id,
    )
