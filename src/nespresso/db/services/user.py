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
        # - Tg -
        self.RegisterTgUser = self.tg_user_repo.CreateTgUser

        # - Nes -
        self.UpsertNesUser = self.nes_user_repo.UpsertNesUsers

        # ----- Read -----
        # - Tg -
        self.GetTgUsersOnCondition = self.tg_user_repo.GetTgUsersOnCondition
        self.GetTgUser = self.tg_user_repo.GetTgUser
        self.GetTgChatIdBy = self.tg_user_repo.GetChatIdBy

        # - Nes -
        self.GetNesUser = self.nes_user_repo.GetNesUser
        self.GetNesUserColumn = self.nes_user_repo.GetNesUserColumn

        # ----- Update -----
        # - Tg -
        self.UpdateTgUser = self.tg_user_repo.UpdateTgUser

        # ----- Delete -----

    # ----- Create -----

    # ----- Read -----
    # - Tg -
    async def CheckTgUserExists(self, chat_id: int) -> bool:
        result = await self.GetTgUser(
            chat_id=chat_id,
            column=TgUser.chat_id,
        )

        return result is not None

    async def GetTgUsername(self, chat_id: int) -> str:
        result = await self.GetTgUser(
            chat_id=chat_id,
            column=TgUser.username,
        )

        return str(result)

    async def GetVerifiedTgUsersChatId(self) -> list[int]:
        result = await self.GetTgUsersOnCondition(
            condition=TgUser.verified,
            column=TgUser.chat_id,
        )

        return result if result else []

    # ----- Update -----

    # ----- Delete -----
