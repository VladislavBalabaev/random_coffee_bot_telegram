from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from nespresso.db.models.message import Message, MessageSide


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def AddMessage(self, chat_id: int, text: str, side: MessageSide) -> None:
        self.session.add(Message(chat_id=chat_id, side=side, text=text))

        await self.session.commit()

    async def GetRecentMessages(self, chat_id: int, limit: int) -> list[Message]:
        result = await self.session.execute(
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(desc(Message.time))
            .limit(limit)
        )

        return list(result.scalars().all())
