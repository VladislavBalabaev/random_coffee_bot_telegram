from nespresso.db.repositories.message import MessageRepository
from nespresso.db.repositories.nes_user import NesUserRepository
from nespresso.db.repositories.tg_user import TgUserRepository
from nespresso.db.session import AsyncSessionLocal
from nespresso.services.message import MessageService
from nespresso.services.user import UserService
from nespresso.services.user_context import UserContextService


async def GetUserContextService() -> UserContextService:
    tg_user_repo = TgUserRepository(AsyncSessionLocal)
    nes_user_repo = NesUserRepository(AsyncSessionLocal)
    message_repo = MessageRepository(AsyncSessionLocal)

    user_service = UserService(tg_user_repo=tg_user_repo, nes_user_repo=nes_user_repo)
    message_service = MessageService(message_repo)

    return UserContextService(user_service, message_service)
