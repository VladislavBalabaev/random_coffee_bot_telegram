from aiogram import types
from aiogram.filters import Filter

from nespresso.core.configs.constants import ADMIN_CHAT_IDS
from nespresso.db.models.tg_user import TgUser
from nespresso.db.services.user_context import user_ctx


class AdminFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.chat.id in ADMIN_CHAT_IDS


async def VerifiedFilter(chat_id: int) -> bool:
    ctx = await user_ctx()

    verified = await ctx.GetTgUser(
        chat_id=chat_id,
        column=TgUser.verified,
    )

    return verified if verified else False
