from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Sequence

from core.config import settings
from core.models import db_helper

from core.schemas.assignment import (
    AssignmentCreate,
    AssignmentRead,
    AssignmentUpdate,
    AssignmentUpdatePartial,
)
from core.schemas.user import UserAuthRead
from crud import assignments as crud

from crud.auth import get_user_id_from_auth, get_current_active_auth_user

router = APIRouter(
    prefix=settings.api.v1.assignments,
    tags=[settings.api.v1.assignments[1:].capitalize()],
)


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
    current_user: Annotated[
        UserAuthRead,
        Depends(get_current_active_auth_user),
    ],
    assignment_in: AssignmentCreate,
):
    return await crud.create_assignment(
        session=session,
        user_id=get_user_id_from_auth(session=session, user_auth=current_user),
        assignment_in=assignment_in,
    )


@router.get(
    "/{assignment_id}/",
    response_model=AssignmentRead,
)
async def get_assignment(
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
    return await crud.get_assignment(
        session=session,
        user_id=get_user_id_from_auth(session=session, user_auth=current_user),
        assignment_id=assignment_id,
    )


@router.get(
    "/",
    response_model=Sequence[AssignmentRead],
)
async def get_assignments(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user: Annotated[
        UserAuthRead,
        Depends(get_current_active_auth_user),
    ],
    group_id: int,
):
    return await crud.get_assignments(
        session=session,
        user_id=get_user_id_from_auth(session=session, user_auth=current_user),
        group_id=group_id,
    )


@router.put("/{assignment_id}/")
async def update_assignment(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user: Annotated[
        UserAuthRead,
        Depends(get_current_active_auth_user),
    ],
    assignment_update: AssignmentUpdate,
    assignment_id: int,
):
    return await crud.update_assignment(
        session=session,
        user_id=get_user_id_from_auth(session=session, user_auth=current_user),
        assignment_id=assignment_id,
        assignment_update=assignment_update,
    )


@router.patch("/{assignment_id}/")
async def update_assignment_partial(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    current_user: Annotated[
        UserAuthRead,
        Depends(get_current_active_auth_user),
    ],
    assignment_update: AssignmentUpdatePartial,
    assignment_id: int,
):
    return await crud.update_assignment(
        session=session,
        user_id=get_user_id_from_auth(session=session, user_auth=current_user),
        assignment_id=assignment_id,
        assignment_update=assignment_update,
        partial=True,
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
    current_user: Annotated[
        UserAuthRead,
        Depends(get_current_active_auth_user),
    ],
    assignment_id: int,
) -> None:
    await crud.delete_assignment(
        session=session,
        user_id=get_user_id_from_auth(session=session, user_auth=current_user),
        assignment_id=assignment_id,
    )
