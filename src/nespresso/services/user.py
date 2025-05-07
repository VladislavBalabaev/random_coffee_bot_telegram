from nespresso.db.repositories.user import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def UsernameById(self, chat_id: int) -> str:
        return "a"

    async def RegisterUser(self, chat_id: int, username: str) -> None:
        # await self.user_repo.Upsert(chat_id, username)
        ...

    ...
