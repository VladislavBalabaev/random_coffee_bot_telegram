from nespresso.db.repositories.user import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def UsernameById(self, user_id: int) -> str:
        return ...

    async def UpsertUser(self, user_id: int, username: str) -> None: ...
