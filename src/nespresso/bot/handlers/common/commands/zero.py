from aiogram import Router, types
from aiogram.filters.state import StateFilter

from nespresso.bot.lib.messaging.stream import (
    MessageContext,
    ReceiveMessage,
    SendMessage,
)

router = Router()


@router.message(StateFilter(None))  # catching all messages with "zero" condition
async def ZeroMessage(message: types.Message) -> None:
    """
    Handles messages that don't match any command or state.
    Notifies the user that they are not in any conversation or command sequence.
    """
    await ReceiveMessage(message=message, context=MessageContext.ZeroMessage)

    await SendMessage(
        message.chat.id,
        "Ты не находишься в какой-либо команде\nВыбери из Menu",
    )
