from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from nespresso.bot.lib.messaging.filters import AdminFilter
from nespresso.bot.lib.messaging.stream import (
    ReceiveMessage,
    SendMessage,
)

router = Router()

_commands = """/logs\nsee logs\n\n
/messages\nsee messages of a user\n\n
/send\nsend message to a user\n\n
/senda\nsend messages to all verified users
"""


@router.message(Command("admin"), StateFilter(None), AdminFilter())
async def CommandAdmin(message: types.Message) -> None:
    await ReceiveMessage(message)

    await SendMessage(chat_id=message.chat.id, text=_commands)
