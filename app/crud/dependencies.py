from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Group

from . import groups as groups_crud


async def validate_group_by_id(
    group_id: Annotated[int, Path],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> Group:
    group = await groups_crud.get_group(session=session, group_id=group_id)
    if group is not None:
        return group

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Group {group_id} not found!",
    )
