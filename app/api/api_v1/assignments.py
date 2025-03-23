from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from core.config import settings
from core.models import db_helper, Assignment
from core.schemas.assignment import (
    AssignmentCreate,
    AssignmentRead,
    AssignmentUpdate,
    AssignmentUpdatePartial,
)
from crud import assignments as crud

router = APIRouter(tags=settings.api.v1.assignments.capitalize())


@router.post(
    "/",
    response_model=AssignmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_assignment(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    assignment_in: AssignmentCreate,
):
    return await crud.create_assignment(session=session, assignment_in=assignment_in)


@router.get(
    "/{assignment_id}/",
    response_model=AssignmentRead,
)
async def get_assignment(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    assignment_id: int,
):
    return await crud.get_assignment(session=session, assignment_id=assignment_id)


@router.get(
    "/",
    response_model=list[AssignmentRead],
)
async def get_assignments(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter()),
    ],
):
    return await crud.get_assignments(session=session)


@router.put("/{assignment_id}/")
async def update_assignment(
    session: Annotated[AsyncSession, Depends(db_helper.dependency_session_getter())],
    assignment_update: AssignmentUpdate,
    assignment: Assignment,
):
    return await crud.update_assignment(
        session=session,
        assignment=assignment,
        assignment_update=assignment_update,
    )


@router.patch("/{assignment_id}/")
async def update_assignment_partial(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    assignment_update: AssignmentUpdatePartial,
    assignment: Assignment,
):
    return await crud.update_assignment(
        session=session,
        assignment=assignment,
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
        Depends(db_helper.session_getter),
    ],
    assignment: Assignment,
) -> None:
    await crud.delete_assignment(session=session, assignment=assignment)
