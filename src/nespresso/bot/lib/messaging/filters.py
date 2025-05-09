from aiogram import types
from aiogram.filters import Filter

from nespresso.core.configs.constants import ADMIN_CHAT_IDS


class AdminFilter(Filter):
    """
    A filter that checks if the message sender is an admin by verifying their chat_id.
    """

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.id in ADMIN_CHAT_IDS
