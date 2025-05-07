from sqlalchemy.ext.asyncio import AsyncSession

from nespresso.db.models.message import Message


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def Smth(self) -> None: ...

    async def Smth2(self) -> list[Message]: ...
