from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

import users.services.email_access as crud
from database import db_helper
from users.services.email_access import verify as crud_verify

router = APIRouter()


@router.get("/{token}")
async def verify(
    token: str,
    session: Annotated[AsyncSession, Depends(db_helper.dependency_session_getter)],
):
    return await crud_verify(token=token, session=session)


@router.get("/reset_password_redirect/{token}")
async def reset_password_redirect(
    token: str,
    new_password: str,
    session: Annotated[AsyncSession, Depends(db_helper.dependency_session_getter)],
):
    return await crud.reset_password_redirect(
        token=token,
        new_password=new_password,
        session=session,
    )


@router.get("/forgot_password_redirect/{token}")
async def forgot_password_redirect(
    token: str,
    new_password: str,
    session: Annotated[AsyncSession, Depends(db_helper.dependency_session_getter)],
):
    return await crud.forgot_password_redirect(
        token=token,
        new_password=new_password,
        session=session,
    )
