from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from nespresso.bot.lib.messaging.stream import (
    MessageContext,
    ReceiveMessage,
    SendMessage,
)

router = Router()


class StartStates(StatesGroup):
    EmailGet = State()
    EmailConfirm = State()


@router.message(Command("start"))
async def CommandStart(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    # check if user already confirmed his email
    await state.set_state(StartStates.EmailGet)

    await SendMessage(
        chat_id=message.chat.id,
        text="Are you a goofy guy?"
    )


@router.message(StateFilter(StartStates.EmailGet), F.content_type == "text")
async def CommandStartEmailGet(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    await SendMessage(
        chat_id=message.chat.id, text="lol", context=MessageContext.UserFailed
    )
