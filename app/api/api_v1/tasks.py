from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Sequence

from core.config import settings
from core.models import db_helper

from core.schemas.task import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
    TaskUpdatePartial,
)
from core.schemas.user import UserAuthRead
from crud import tasks as crud

from crud.auth import get_user_id_from_auth, get_current_active_auth_user

router = APIRouter(
    prefix=settings.api.v1.tasks,
    tags=[settings.api.v1.tasks[1:].capitalize()],
)


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
    current_user: Annotated[
        UserAuthRead,
        Depends(get_current_active_auth_user),
    ],
    task_in: TaskCreate,
):
    return await crud.create_task(
        session=session,
        user_id=get_user_id_from_auth(session=session, user_auth=current_user),
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
    current_user: Annotated[
        UserAuthRead,
        Depends(get_current_active_auth_user),
    ],
    task_id: int,
):
    return await crud.get_task(
        session=session,
        user_id=get_user_id_from_auth(session=session, user_auth=current_user),
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
    current_user: Annotated[
        UserAuthRead,
        Depends(get_current_active_auth_user),
    ],
    assignment_id: int,
):
    return await crud.get_tasks(
        session=session,
        user_id=get_user_id_from_auth(session=session, user_auth=current_user),
        assignment_id=assignment_id,
    )


@router.put("/{task_id}/")
async def update_task(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user: Annotated[
        UserAuthRead,
        Depends(get_current_active_auth_user),
    ],
    task_update: TaskUpdate,
    task_id: int,
):
    return await crud.update_task(
        session=session,
        user_id=get_user_id_from_auth(session=session, user_auth=current_user),
        task_id=task_id,
        task_update=task_update,
    )


@router.patch("/{task_id}/")
async def update_task_partial(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user: Annotated[
        UserAuthRead,
        Depends(get_current_active_auth_user),
    ],
    task_update: TaskUpdatePartial,
    task_id: int,
):
    return await crud.update_task(
        session=session,
        user_id=get_user_id_from_auth(session=session, user_auth=current_user),
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
    current_user: Annotated[
        UserAuthRead,
        Depends(get_current_active_auth_user),
    ],
    task_id: int,
) -> None:
    await crud.delete_task(
        session=session,
        user_id=get_user_id_from_auth(session=session, user_auth=current_user),
        task_id=task_id,
    )
