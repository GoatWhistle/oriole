from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from features import Group, Account
from features.chat.models.chat import Chat

from features.groups.validators import (
    get_group_or_404,
)


async def create_chat_for_group(
    session: AsyncSession,
    group_id: int,
    account_id: int,
) -> Chat:
    group = await get_group_or_404(session, group_id)
    if group.chat is not None:
        return group.chat
    chat = Chat(
        group_id=group.id,
        creator_id=account_id,
    )
    session.add(chat)
    await session.commit()
    await session.refresh(chat)
    return chat


async def get_users_chat(
    session: AsyncSession,
    user_id: int,
):
    stmt = (
        select(Chat)
        .join(Group, Chat.group_id == Group.id)
        .join(Account, Account.group_id == Group.id)
        .where(Account.user_id == user_id)
    )
    result = await session.execute(stmt)
    chats = result.scalars().all()
    return chats


async def get_chat_by_group_id(session: AsyncSession, group_id: int):
    stmt = select(Chat).where(Chat.group_id == group_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
