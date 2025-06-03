from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from nespresso.bot.lib.messaging.filters import AdminFilter
from nespresso.bot.lib.messaging.stream import (
    MessageContext,
    ReceiveMessage,
    SendMessage,
    SendMessageToGroup,
)
from nespresso.db.services.user_context import user_ctx

router = Router()


class SendaStates(StatesGroup):
    Message = State()


@router.message(Command("senda"), StateFilter(None), AdminFilter())
async def CommandSenda(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    await SendMessage(chat_id=message.chat.id, text="Input text of message")
    await state.set_state(SendaStates.Message)


@router.message(StateFilter(SendaStates.Message), F.content_type == "text")
async def CommandSendaMessage(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    if message.text is None:
        await SendMessage(
            chat_id=message.chat.id,
            text="Provide text",
            context=MessageContext.UserFailed,
        )
        return

    ctx = await user_ctx()
    chat_ids = await ctx.GetRegisteredTgUsersChatId()

    await SendMessageToGroup(chat_ids=chat_ids, text=message.text)

    await SendMessage(chat_id=message.chat.id, text="Done")
    await state.clear()
