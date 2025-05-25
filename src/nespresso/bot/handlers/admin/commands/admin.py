from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from nespresso.bot.lib.messaging.filters import AdminFilter
from nespresso.bot.lib.messaging.stream import (
    ReceiveMessage,
    SendMessage,
)

router = Router()

_commands = """/logs - see logs,
/messages - see messages of a user,
/send - send message to a user,
/senda - send messages to all registered users,
"""


@router.message(Command("admin"), StateFilter(None), AdminFilter())
async def CommandAdmin(message: types.Message) -> None:
    await ReceiveMessage(message)

    await SendMessage(chat_id=message.chat.id, text=_commands)
