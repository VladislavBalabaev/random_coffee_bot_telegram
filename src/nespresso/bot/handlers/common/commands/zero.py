from aiogram import F, Router, types

from nespresso.bot.lib.messaging.stream import (
    MessageContext,
    ReceiveMessage,
    SendMessage,
)

router = Router()


@router.message(F.content_type == "text")  # catching all messages with "zero" condition
async def ZeroMessageText(message: types.Message) -> None:
    """
    Handles messages that don't match any command or state.
    Notifies the user that they are not in any conversation or command sequence.
    """
    await ReceiveMessage(message=message, context=MessageContext.ZeroMessage)

    await SendMessage(
        message.chat.id,
        "Ты не находишься в какой-либо команде\nВыбери из Menu",
    )


@router.message()
async def ZeroMessageOther(message: types.Message) -> None:
    await ReceiveMessage(message=message, context=MessageContext.NoText)

    await SendMessage(
        chat_id=message.chat.id,
        text="Бот определяет только текст"
    )
