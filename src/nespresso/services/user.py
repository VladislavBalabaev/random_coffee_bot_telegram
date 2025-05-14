from typing import Any

from sqlalchemy.orm.attributes import InstrumentedAttribute

from nespresso.db.models.nes_user import NesUser
from nespresso.db.models.tg_user import TgUser
from nespresso.db.repositories.nes_user import NesUserRepository
from nespresso.db.repositories.tg_user import TgUserRepository


class UserService:
    def __init__(
        self, tg_user_repo: TgUserRepository, nes_user_repo: NesUserRepository
    ):
        self.tg_user_repo = tg_user_repo
        self.nes_user_repo = nes_user_repo

    # ----- Create -----

    async def RegisterTgUser(
        self, chat_id: int, username: str | None = None, full_name: str | None = None
    ) -> None:
        await self.tg_user_repo.CreateTgUser(
            chat_id=chat_id, username=username, full_name=full_name
        )

    # - Nes -
    async def UpsertNesUser(
        self,
    ) -> None: ...

    # ----- Read -----
    async def CheckTgUserExists(self, chat_id: int) -> bool:
        result = await self.tg_user_repo.GetTgUserColumn(chat_id, TgUser.chat_id)

        return result is not None

    async def GetTgUser(self, chat_id: int) -> TgUser | None:
        return await self.tg_user_repo.GetTgUser(chat_id)

    async def GetTgUserColumn(
        self, chat_id: int, column: InstrumentedAttribute[Any]
    ) -> Any | None:
        return await self.tg_user_repo.GetTgUserColumn(chat_id, column)

    async def GetTgUsername(self, chat_id: int) -> str:
        result = await self.tg_user_repo.GetTgUserColumn(
            chat_id=chat_id, column=TgUser.username
        )

        return str(result)

    # - Nes -
    async def GetNesUser(self, nes_id: int) -> NesUser | None:
        return await self.nes_user_repo.GetNesUser(nes_id)

    async def GetNesUserColumn(
        self, nes_id: int, column: InstrumentedAttribute[Any]
    ) -> Any | None:
        return await self.nes_user_repo.GetNesUserColumn(nes_id, column)

    # ----- Update -----

    async def UpdateTgUser(
        self, chat_id: int, column: InstrumentedAttribute[Any], value: Any
    ) -> None:
        await self.tg_user_repo.UpdateTgUser(
            chat_id=chat_id, column=column, value=value
        )

    # ----- Delete -----
