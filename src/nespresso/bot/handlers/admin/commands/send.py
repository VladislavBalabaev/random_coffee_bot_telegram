from aiogram import F, Router, types
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from nespresso.bot.lib.messaging.filters import AdminFilter
from nespresso.bot.lib.messaging.stream import (
    MessageContext,
    ReceiveMessage,
    SendMessage,
)
from nespresso.core.services import user_ctx

router = Router()


class SendStates(StatesGroup):
    Message = State()


@router.message(Command("send"), StateFilter(None), AdminFilter())
async def CommandSend(
    message: types.Message, command: CommandObject, state: FSMContext
) -> None:
    await ReceiveMessage(message)

    if not command.args or len(command.args.split()) != 1:
        await SendMessage(
            chat_id=message.chat.id,
            text="Iclude tg username:\n/send @vbalab",
            context=MessageContext.UserFailed,
        )
        return

    ctx = await user_ctx()
    chat_id = await ctx.GetTgChatIdBy(tg_username=command.args.replace("@", "").strip())

    if chat_id is None:
        await SendMessage(
            chat_id=message.chat.id,
            text="User with such credentials doesn't exist.\nAborting",
            context=MessageContext.UserFailed,
        )
        await state.clear()
        return

    await SendMessage(chat_id=message.chat.id, text="Input text of message")
    await state.set_state(SendStates.Message)
    await state.set_data({"chat_id": chat_id})


@router.message(StateFilter(SendStates.Message), F.content_type == "text")
async def CommandSendMessage(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    if message.text is None:
        await SendMessage(
            chat_id=message.chat.id,
            text="Provide text",
            context=MessageContext.UserFailed,
        )
        return

    data = await state.get_data()

    await SendMessage(chat_id=data["chat_id"], text=message.text)

    await SendMessage(chat_id=message.chat.id, text="Done")
    await state.clear()
