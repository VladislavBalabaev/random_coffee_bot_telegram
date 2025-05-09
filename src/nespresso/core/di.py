from nespresso.db.repositories.message import MessageRepository
from nespresso.db.repositories.user import UserRepository
from nespresso.db.session import AsyncSessionLocal
from nespresso.services.message import MessageService
from nespresso.services.user import UserService
from nespresso.services.user_context import UserContextService


async def GetUserContextService() -> UserContextService:
    user_repo = UserRepository(AsyncSessionLocal)
    message_repo = MessageRepository(AsyncSessionLocal)

    user_service = UserService(user_repo)
    message_service = MessageService(message_repo)

    return UserContextService(user_service, message_service)
