from fastapi import (
    APIRouter,
    Depends,
)

from typing import Annotated

from core.models import db_helper

from sqlalchemy.ext.asyncio import AsyncSession

from crud.email_access import verify as crud_verify

router = APIRouter()


@router.get("/{token}")
async def verify(
    token: str,
    session: Annotated[AsyncSession, Depends(db_helper.dependency_session_getter)],
):
    return await crud_verify(token=token, session=session)
