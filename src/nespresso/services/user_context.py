from nespresso.db.models.message import Message
from nespresso.services.message import MessageService
from nespresso.services.user import UserService


class UserContextService(UserService, MessageService):
    """
    Combines UserService and MessageService into a single context service.
    Inherits methods from both services.
    """

    def __init__(self, user_service: UserService, message_service: MessageService):
        # Initialize both parent classes explicitly
        UserService.__init__(
            self,
            tg_user_repo=user_service.tg_user_repo,
            nes_user_repo=user_service.nes_user_repo,
        )
        MessageService.__init__(self, message_service.message_repo)

    async def GetRecentMessages(
        self,
        chat_id: int | None = None,
        tg_username: str | None = None,
        nes_id: int | None = None,
        nes_email: str | None = None,
        limit: int = 10,
    ) -> list[Message]:
        if chat_id is None:
            chat_id = await self.GetChatIdBy(
                tg_username=tg_username, nes_id=nes_id, nes_email=nes_email
            )

            if chat_id is None:
                return []

        result = await self.message_repo.GetRecentMessages(chat_id, limit)

        return result
