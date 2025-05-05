from nespresso.db.repositories.message import MessageRepository


class MessageService:
    def __init__(self, message_repo: MessageRepository):
        self.message_repo = message_repo

    async def Smth(self, user_id: int) -> str:
        ...
        return "a"
