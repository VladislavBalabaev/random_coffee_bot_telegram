from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from nespresso.bot.lib.messaging.stream import (
    MessageContext,
    ReceiveMessage,
    SendMessage,
)

router = Router()


@router.message(Command("start"))
async def CommandStart(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    await SendMessage(
        chat_id=message.chat.id, text="приветики", context=MessageContext.UserFailed
    )

# USE F.content_type == "text"
