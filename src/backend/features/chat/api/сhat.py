from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.chat.dependencies.dependencies import get_current_account_id
from features.users.services.auth import get_current_active_auth_user_id
from ..crud import chat as crud

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chat(
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_account_id),
):
    chat = await crud.create_chat_for_group(session, group_id, user_id)
    return chat


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users_chat(
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(
        get_current_active_auth_user_id,
    ),
):
    return await crud.get_users_chat(session, user_id)
