from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nespresso.db.models.user import NesUser, TgUser, User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def GetById(self, chat_id: int) -> TgUser | None:
        result = await self.session.execute(
            select(TgUser).where(TgUser.chat_id == chat_id)
        )

        return result.scalar_one_or_none()

    async def Upsert(self) -> None:
        User
        ...

    async def GetNesInfo(self) -> None:
        NesUser
        ...

    async def ActualizeUsers(self) -> None: ...

    ...
