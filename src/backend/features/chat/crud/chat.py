from sqlalchemy.ext.asyncio import AsyncSession

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
