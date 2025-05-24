from nespresso.db.models.message import MessageSide
from nespresso.db.repositories.message import MessageRepository


class MessageService:
    def __init__(self, message_repo: MessageRepository):
        self.message_repo = message_repo

        self.GetRecentMessages = self.message_repo.GetRecentMessages

    async def RegisterIncomingMessage(self, chat_id: int, text: str) -> None:
        await self.message_repo.AddMessage(
            chat_id=chat_id, text=text, side=MessageSide.User
        )

    async def RegisterOutgoingMessage(self, chat_id: int, text: str) -> None:
        await self.message_repo.AddMessage(
            chat_id=chat_id, text=text, side=MessageSide.Bot
        )
