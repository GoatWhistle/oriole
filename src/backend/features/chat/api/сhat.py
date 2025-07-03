from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.chat.crud.chat import create_chat_for_group
from features.chat.dependencies.dependencies import get_current_account_id

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chat(
    group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_account_id),
):
    chat = await create_chat_for_group(session, group_id, user_id)
    return chat
