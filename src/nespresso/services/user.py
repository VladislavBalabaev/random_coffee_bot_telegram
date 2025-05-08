from typing import Any

from sqlalchemy.orm.attributes import InstrumentedAttribute

from nespresso.db.models.user import NesUser, TgUser
from nespresso.db.repositories.user import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    # ----- Create -----

    async def RegisterTgUser(
        self, chat_id: int, username: str | None = None, full_name: str | None = None
    ) -> None:
        await self.user_repo.CreateTgUser(
            chat_id=chat_id, username=username, full_name=full_name
        )

    # ----- Read -----
    async def CheckTgUserExists(self, chat_id: int) -> bool:
        result = await self.user_repo.GetTgUserColumn(chat_id, TgUser.chat_id)

        return result is not None

    async def GetTgUser(self, chat_id: int) -> TgUser | None:
        return await self.user_repo.GetTgUser(chat_id)

    async def GetTgUserColumn(
        self, chat_id: int, column: InstrumentedAttribute[Any]
    ) -> Any | None:
        return await self.user_repo.GetTgUserColumn(chat_id, column)

    async def GetNesUser(self, nes_id: int) -> NesUser | None:
        return await self.user_repo.GetNesUser(nes_id)

    async def GetNesUserColumn(
        self, nes_id: int, column: InstrumentedAttribute[Any]
    ) -> Any | None:
        return await self.user_repo.GetNesUserColumn(nes_id, column)

    async def GetTgUsername(self, chat_id: int) -> str:
        result = await self.user_repo.GetTgUserColumn(
            chat_id=chat_id, column=TgUser.username
        )

        return str(result)

    # ----- Update -----

    async def UpdateTgUser(
        self, chat_id: int, column: InstrumentedAttribute[Any], value: Any
    ) -> None:
        await self.user_repo.UpdateTgUser(chat_id=chat_id, column=column, value=value)

    # ----- Delete -----
