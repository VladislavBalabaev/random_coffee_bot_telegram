from aiogram import Router, types
from aiogram.filters.state import StateFilter

from nespresso.bot.lib.messaging.checks import checker
from nespresso.bot.lib.messaging.stream import SendMessage

router = Router()


@router.message(StateFilter(None))  # catching all messages with "zero" condition
@checker
async def ZeroMessage(message: types.Message) -> None:
    """
    Handles messages that don't match any command or state.
    Notifies the user that they are not in any conversation or command sequence.
    """
    await SendMessage(
        message.chat.id,
        "Ты не находишься в какой-либо команде\nВыбери что-нибудь из Menu",
    )
