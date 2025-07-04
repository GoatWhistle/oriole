from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from features import Message


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_messages_by_group(self, group_id: int):
        stmt = (
            select(Message)
            .where(Message.group_id == group_id)
            .order_by(Message.timestamp)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, message_id: int):
        return await self.session.get(Message, message_id)

    async def save_new_message(self, message: Message):
        self.session.add(message)
        await self.session.commit()

    async def delete(self, message: Message):
        await self.session.delete(message)
        await self.session.commit()

    async def update_message(self, message: Message, new_text: str):
        message.text = new_text
        await self.session.commit()
