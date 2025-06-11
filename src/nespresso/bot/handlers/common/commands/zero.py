from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from nespresso.bot.lib.message.io import ContextIO, SendMessage

router = Router()


@router.message(F.content_type == "text")
async def ZeroMessageText(message: types.Message) -> None:
    await SendMessage(
        chat_id=message.chat.id,
        text="You're not in a command right now.\nPick something from the Menu",
        context=ContextIO.ZeroMessage,
    )


@router.message()
async def NoTextMessage(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state is None:
        text = "The bot only works with text messages.\nPick something from the Menu"
    else:
        text = "The bot only works with text messages\nTry again"

    await SendMessage(chat_id=message.chat.id, text=text, context=ContextIO.NoText)
