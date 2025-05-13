from fastapi import (
    APIRouter,
    Depends,
)

from typing import Annotated

import crud.email_access as crud
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


@router.get("/reset_password_redirect/{token}")
async def verify(
    token: str,
    new_password: str,
    session: Annotated[AsyncSession, Depends(db_helper.dependency_session_getter)],
):
    return await crud.reset_password_redirect(
        token=token,
        new_password=new_password,
        session=session,
    )
