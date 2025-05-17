from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Sequence, Optional

from core.schemas.task import TaskReadPartial

from core.schemas.assignment import (
    AssignmentCreate,
    AssignmentRead,
    AssignmentReadPartial,
    AssignmentUpdate,
    AssignmentUpdatePartial,
)

from core.models import db_helper
from crud.auth import get_current_active_auth_user_id
from crud import assignments as crud


router = APIRouter()


@router.post(
    "/",
    response_model=AssignmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_assignment(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    user_timezone: str,
    assignment_in: AssignmentCreate,
):
    return await crud.create_assignment(
        session=session,
        user_id=user_id,
        user_timezone=user_timezone,
        assignment_in=assignment_in,
    )


@router.get(
    "/{assignment_id}/",
    response_model=AssignmentRead,
    status_code=status.HTTP_200_OK,
)
async def get_assignment_by_id(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    user_timezone: str,
    assignment_id: int,
):
    return await crud.get_assignment_by_id(
        session=session,
        user_id=user_id,
        user_timezone=user_timezone,
        assignment_id=assignment_id,
    )


@router.get(
    "/",
    response_model=Sequence[AssignmentReadPartial],
    status_code=status.HTTP_200_OK,
)
async def get_user_assignments(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
):
    return await crud.get_user_assignments(
        session=session,
        user_id=user_id,
    )


@router.put(
    "/{assignment_id}/",
    response_model=AssignmentRead,
    status_code=status.HTTP_200_OK,
)
async def update_assignment(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    user_timezone: str,
    assignment_update: AssignmentUpdate,
    assignment_id: int,
):
    return await crud.update_assignment(
        session=session,
        user_id=user_id,
        user_timezone=user_timezone,
        assignment_id=assignment_id,
        assignment_update=assignment_update,
        is_partial=False,
    )


@router.patch(
    "/{assignment_id}/",
    response_model=AssignmentRead,
    status_code=status.HTTP_200_OK,
)
async def update_assignment_partial(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    user_timezone: str,
    assignment_update: AssignmentUpdatePartial,
    assignment_id: int,
):
    return await crud.update_assignment(
        session=session,
        user_id=user_id,
        user_timezone=user_timezone,
        assignment_id=assignment_id,
        assignment_update=assignment_update,
        is_partial=True,
    )


@router.delete(
    "/{assignment_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_assignment(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    assignment_id: int,
) -> None:
    await crud.delete_assignment(
        session=session,
        user_id=user_id,
        assignment_id=assignment_id,
    )


@router.get(
    "/{assignment_id}/tasks/",
    response_model=Sequence[TaskReadPartial],
    status_code=status.HTTP_200_OK,
)
async def get_tasks_in_assignment(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    assignment_id: int,
    is_correct: Optional[bool] = None,
) -> Sequence[TaskReadPartial]:
    return await crud.get_tasks_in_assignment(
        session=session,
        user_id=user_id,
        assignment_id=assignment_id,
        is_correct=is_correct,
    )
