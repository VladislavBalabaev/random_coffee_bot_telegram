from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nespresso.db.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def GetById(self, user_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))

        return result.scalar_one_or_none()

    async def Upsert(self, user_id: int, username: str) -> User:
        return ...
