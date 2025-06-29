from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.users.services import email_access as service

router = APIRouter()


@router.get("/{token}")
async def verify(
        token: str,
        session: Annotated[AsyncSession, Depends(db_helper.dependency_session_getter)],
):
    return await service.verify(token=token, session=session)


@router.get("/reset_password_redirect/{token}")
async def reset_password_redirect(
        token: str,
        new_password: str,
        session: Annotated[AsyncSession, Depends(db_helper.dependency_session_getter)],
):
    return await service.reset_password_redirect(
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
    return await service.forgot_password_redirect(
        token=token,
        new_password=new_password,
        session=session,
    )
