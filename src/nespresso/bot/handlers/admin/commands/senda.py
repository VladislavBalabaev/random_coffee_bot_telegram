from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from nespresso.bot.lib.messaging.filters import AdminFilter
from nespresso.bot.lib.messaging.stream import (
    PersonalMsg,
    ReceiveMessage,
    SendMessage,
    SendMessagesToGroup,
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
    assert message.text is not None

    ctx = await user_ctx()
    chat_ids = await ctx.GetVerifiedTgUsersChatId()

    messages = [PersonalMsg(chat_id=chat_id, text=message.text) for chat_id in chat_ids]
    await SendMessagesToGroup(messages)

    await SendMessage(chat_id=message.chat.id, text="Done")
    await state.clear()
