from nespresso.services.message import MessageService
from nespresso.services.user import UserService


class UserContextService:
    def __init__(self, user_service: UserService, message_service: MessageService):
        self.user_service = user_service
        self.messaging_service = message_service

    async def RegisterIncoming(self, user_id: int, text: str, username: str) -> None:
        # await self.user_service.upsert_user(user_id, username)
        # await self.messaging_service.insert_message(user_id, text, "in")
        ...

    async def RegisterOutgoing(self, user_id: int, text: str) -> None: ...

    async def GetUsernameById(self, user_id: int) -> str:
        ...
        return "a"
