from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from nespresso.db.models.message import Message, MessageSide


class MessageRepository:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def AddMessage(
        self, message_id: int, chat_id: int, text: str, side: MessageSide
    ) -> None:
        async with self.session() as session:
            session.add(
                Message(
                    message_id=message_id,
                    chat_id=chat_id,
                    side=side,
                    text=text,
                )
            )

            await session.commit()

    async def GetRecentMessages(self, chat_id: int, limit: int) -> list[Message]:
        async with self.session() as session:
            result = await session.execute(
                select(Message)
                .where(Message.chat_id == chat_id)
                .order_by(desc(Message.time))
                .limit(limit)
            )

            return list(result.scalars().all())
