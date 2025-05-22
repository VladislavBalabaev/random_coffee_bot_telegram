from enum import Enum, auto

from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.exc import ProgrammingError

from nespresso.bot.lib.messaging.file import SendTemporaryFileFromText, ToJSONText
from nespresso.bot.lib.messaging.filters import AdminFilter
from nespresso.bot.lib.messaging.keyboard import CreateKeyboard
from nespresso.bot.lib.messaging.stream import (
    MessageContext,
    ReceiveMessage,
    SendMessage,
)
from nespresso.core.services import user_ctx

router = Router()


class MessagesStates(StatesGroup):
    Choice = State()
    Credentials = State()
    Limit = State()


class MessageIdentification(Enum):
    chat_id = auto()
    tg_username = auto()
    nes_id = auto()
    nes_email = auto()

    @classmethod
    def HasName(cls, name: str) -> bool:
        return name in cls.__members__


@router.message(Command("messages"), StateFilter(None), AdminFilter())
async def CommandMessages(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    await state.set_state(MessagesStates.Choice)

    keyboard = CreateKeyboard(MessageIdentification)

    await SendMessage(
        chat_id=message.chat.id, text="Select ID type", reply_markup=keyboard
    )


@router.message(StateFilter(MessagesStates.Choice), F.content_type == "text")
async def CommandMessagesChoice(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    if not message.text or not MessageIdentification.HasName(message.text):
        keyboard = CreateKeyboard(MessageIdentification, max_buttons_per_row=4)

        await SendMessage(
            chat_id=message.chat.id,
            text="Select ID type from provided",
            context=MessageContext.UserFailed,
            reply_markup=keyboard,
        )

        return

    await state.set_data({"identification": message.text})

    await state.set_state(MessagesStates.Credentials)

    await SendMessage(
        chat_id=message.chat.id,
        text=f"Provide {message.text} of a user",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(StateFilter(MessagesStates.Credentials), F.content_type == "text")
async def CommandMessagesCredentials(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    data = await state.get_data()
    data = {data["identification"]: message.text}

    ctx = await user_ctx()

    try:
        messages = await ctx.GetRecentMessages(**data, limit=1)
        exists = len(messages) > 0
    except ProgrammingError:
        exists = False

    if not exists:
        await SendMessage(
            chat_id=message.chat.id,
            text="User with such credentials doesn't exist.\nAborting",
            context=MessageContext.UserFailed,
        )

        await state.clear()

        return

    await state.set_data(data)
    await state.set_state(MessagesStates.Limit)

    await SendMessage(
        chat_id=message.chat.id,
        text="Set limit on how many recent messages you request, e.g. 50",
    )


@router.message(StateFilter(MessagesStates.Limit), F.content_type == "text")
async def CommandMessagesLimit(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    if not message.text or not message.text.strip(" ").isdigit():
        await SendMessage(
            chat_id=message.chat.id,
            text="Limit should be a number, e.g. 50\nTry again",
            context=MessageContext.UserFailed,
        )

        return

    await SendMessage(
        chat_id=message.chat.id,
        text="Doing query, please, wait",
    )

    limit = int(message.text.strip(" "))
    data = await state.get_data()

    ctx = await user_ctx()
    messages = await ctx.GetRecentMessages(**data, limit=limit)

    messages_dict = [m.IntoDict() for m in messages]
    messages_str = ToJSONText(messages_dict)

    await state.clear()

    await SendTemporaryFileFromText(chat_id=message.chat.id, text=messages_str)
