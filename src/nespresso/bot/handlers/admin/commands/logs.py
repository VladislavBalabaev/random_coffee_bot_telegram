from aiogram import Router, types
from aiogram.filters.command import Command

from nespresso.bot.lib.messaging.filters import AdminFilter
from nespresso.bot.lib.messaging.stream import (
    ReceiveMessage,
    SendDocument,
)
from nespresso.core.configs.paths import PATH_LOGS

router = Router()


@router.message(Command("logs"), AdminFilter())
async def CommandLogs(message: types.Message) -> None:
    await ReceiveMessage(message)

    await SendDocument(chat_id=message.chat.id, document=types.FSInputFile(PATH_LOGS))
