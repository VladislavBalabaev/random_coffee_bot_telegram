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
    Error = State()


@router.message(StateFilter(None), Command("start"))
async def CommandStart(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    # check if user already confirmed his email

    await SendMessage(chat_id=message.chat.id, text="Are you a goofy guy?")
    await state.set_state(StartStates.EmailGet)


@router.message(StateFilter(StartStates.EmailGet), F.content_type == "text")
async def CommandStartEmailGet(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    await SendMessage(
        chat_id=message.chat.id, text="lol", context=MessageContext.UserFailed
    )
    await state.set_state(StartStates.Error)


@router.message(StateFilter(StartStates.Error), F.content_type == "text")
async def CommandStartCheckError(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    raise ValueError("LOOOOOOOOOOOL")

    await SendMessage(
        chat_id=message.chat.id, text="lol", context=MessageContext.UserFailed
    )
    await state.clear()


# USE: F.content_type == "text"


# -------------

# from enum import Enum, auto

# from aiogram import F, Router, types
# from aiogram.filters.command import Command
# from aiogram.filters.state import StateFilter
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup

# from nespresso.bot.lib.messaging.file import SendTemporaryFileFromText, ToJSONText
# from nespresso.bot.lib.messaging.filters import AdminFilter
# from nespresso.bot.lib.messaging.keyboard import CreateKeyboard
# from nespresso.bot.lib.messaging.stream import (
#     MessageContext,
#     ReceiveMessage,
#     SendMessage,
# )
# from nespresso.core.services import user_ctx

# router = Router()


# class MessagesStates(StatesGroup):
#     Choice = State()
#     Credentials = State()
#     Limit = State()


# class MessageIdentification(Enum):
#     chat_id = auto()
#     tg_username = auto()
#     nes_id = auto()
#     nes_email = auto()

#     @classmethod
#     def HasName(cls, name: str) -> bool:
#         return name in cls.__members__


# @router.message(Command("messages"), StateFilter(None), AdminFilter())
# async def CommandMessages(message: types.Message, state: FSMContext) -> None:
#     await ReceiveMessage(message)

#     keyboard = CreateKeyboard(MessageIdentification)

#     await SendMessage(
#         chat_id=message.chat.id, text="Select ID type", reply_markup=keyboard
#     )
#     await state.set_state(MessagesStates.Choice)


# @router.message(StateFilter(MessagesStates.Choice), F.content_type == "text")
# async def CommandMessagesChoice(message: types.Message, state: FSMContext) -> None:
#     await ReceiveMessage(message)

#     if not message.text or not MessageIdentification.HasName(message.text):
#         keyboard = CreateKeyboard(MessageIdentification, max_buttons_per_row=4)

#         await SendMessage(
#             chat_id=message.chat.id,
#             text="Select ID type from provided",
#             context=MessageContext.UserFailed,
#             reply_markup=keyboard,
#         )

#         return

#     await SendMessage(
#         chat_id=message.chat.id,
#         text=f"Provide {message.text} of a user",
#         reply_markup=types.ReplyKeyboardRemove(),
#     )
#     await state.set_data({"identification": message.text})
#     await state.set_state(MessagesStates.Credentials)


# @router.message(StateFilter(MessagesStates.Credentials), F.content_type == "text")
# async def CommandMessagesCredentials(message: types.Message, state: FSMContext) -> None:
#     await ReceiveMessage(message)

#     data = await state.get_data()
#     idtype = data["identification"]

#     if message.text is None:
#         await SendMessage(
#             chat_id=message.chat.id,
#             text=f"Provide {idtype}",
#             context=MessageContext.UserFailed,
#         )

#         return

#     ctx = await user_ctx()
#     chat_id = await ctx.GetTgChatIdBy(chat_id=int(message.text))

#     if chat_id is None:
#         await SendMessage(
#             chat_id=message.chat.id,
#             text="User with such credentials doesn't exist.\nAborting",
#             context=MessageContext.UserFailed,
#         )

#         await state.clear()
#         return

#     await SendMessage(
#         chat_id=message.chat.id,
#         text="Set limit on how many recent messages you request, e.g. 50",
#     )
#     await state.set_data({"chat_id": chat_id})
#     await state.set_state(MessagesStates.Limit)


# @router.message(StateFilter(MessagesStates.Limit), F.content_type == "text")
# async def CommandMessagesLimit(message: types.Message, state: FSMContext) -> None:
#     await ReceiveMessage(message)

#     if not message.text or not message.text.strip(" ").isdigit():
#         await SendMessage(
#             chat_id=message.chat.id,
#             text="Limit should be a number, e.g. 50\nTry again",
#             context=MessageContext.UserFailed,
#         )

#         return

#     limit = int(message.text.strip(" "))
#     data = await state.get_data()

#     ctx = await user_ctx()

#     messages = await ctx.GetRecentMessages(chat_id=data["chat_id"], limit=limit)
#     messages_dict = [m.IntoDict() for m in messages]
#     messages_str = ToJSONText(messages_dict)

#     await SendTemporaryFileFromText(chat_id=message.chat.id, text=messages_str)
#     await state.clear()
