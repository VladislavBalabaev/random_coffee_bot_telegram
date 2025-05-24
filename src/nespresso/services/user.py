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

        # ----- Read -----
        # - Tg -
        self.GetTgChatIdBy = self.tg_user_repo.GetChatIdBy
        self.GetTgUser = self.tg_user_repo.GetTgUser
        self.GetTgUserColumn = self.tg_user_repo.GetTgUserColumn

        # - Nes -
        self.GetNesUser = self.nes_user_repo.GetNesUser
        self.GetNesUserColumn = self.nes_user_repo.GetNesUserColumn

        # ----- Update -----
        # - Tg -
        self.UpdateTgUser = self.tg_user_repo.UpdateTgUser

        # ----- Delete -----

    # ----- Create -----
    # - Tg -
    async def RegisterTgUser(
        self, chat_id: int, username: str | None = None, full_name: str | None = None
    ) -> None:
        await self.tg_user_repo.CreateTgUser(
            chat_id=chat_id, username=username, full_name=full_name
        )

    # - Nes -
    async def UpsertNesUser(self, user: NesUser) -> None:
        await self.nes_user_repo.UpsertNesUsers(users=user)

    # ----- Read -----
    # - Tg -
    async def CheckTgUserExists(self, chat_id: int) -> bool:
        result = await self.tg_user_repo.GetTgUserColumn(chat_id, TgUser.chat_id)

        return result is not None

    async def GetTgUsername(self, chat_id: int) -> str:
        result = await self.tg_user_repo.GetTgUserColumn(
            chat_id=chat_id, column=TgUser.username
        )

        return str(result)

    # ----- Update -----

    # ----- Delete -----
