from nespresso.db.repositories.message import MessageRepository
from nespresso.db.repositories.user import UserRepository
from nespresso.db.session import AsyncSessionLocal
from nespresso.services.message import MessageService
from nespresso.services.user import UserService
from nespresso.services.user_context import UserContextService


async def GetUserContextService() -> UserContextService:
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        message_repo = MessageRepository(session)

        user_service = UserService(user_repo)
        message_service = MessageService(message_repo)

        return UserContextService(user_service, message_service)
