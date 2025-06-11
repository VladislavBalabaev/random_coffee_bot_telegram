from aiogram import F, Router, types
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from nespresso.bot.lib.message.filters import AdminFilter
from nespresso.bot.lib.message.io import ContextIO, SendMessage
from nespresso.db.services.user_context import GetUserContextService

router = Router()


class SendStates(StatesGroup):
    Message = State()


@router.message(Command("send"), StateFilter(None), AdminFilter())
async def CommandSend(
    message: types.Message,
    command: CommandObject,
    state: FSMContext,
) -> None:
    if not command.args or len(command.args.split()) != 1:
        await SendMessage(
            chat_id=message.chat.id,
            text="Include tg username:\n/send @vbalab",
            context=ContextIO.UserFailed,
        )
        return

    ctx = await GetUserContextService()
    chat_id = await ctx.GetTgChatIdBy(tg_username=command.args.replace("@", "").strip())

    if chat_id is None:
        await SendMessage(
            chat_id=message.chat.id,
            text="User with such credentials doesn't exist.\nAborting",
            context=ContextIO.UserFailed,
        )
        await state.clear()
        return

    await SendMessage(chat_id=message.chat.id, text="Input text of message")

    await state.set_state(SendStates.Message)
    await state.set_data({"chat_id": chat_id})


@router.message(StateFilter(SendStates.Message), F.content_type == "text")
async def CommandSendMessage(message: types.Message, state: FSMContext) -> None:
    assert message.text is not None

    data = await state.get_data()

    output = await SendMessage(chat_id=data["chat_id"], text=message.text)

    if output:
        await SendMessage(chat_id=message.chat.id, text="Successful")
    else:
        await SendMessage(chat_id=message.chat.id, text="Unsuccessful")

    await state.clear()
