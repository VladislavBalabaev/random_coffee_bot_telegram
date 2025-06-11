import asyncio
import logging
from dataclasses import dataclass
from enum import Enum

from aiogram import types
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters.callback_data import CallbackData
from aiolimiter import AsyncLimiter

from nespresso.bot.lib.chat.username import GetChatTgUsername
from nespresso.bot.lifecycle.creator import bot
from nespresso.db.services.user_context import user_ctx


class MsgContext(str, Enum):
    No = ""
    Error = " \033[91m[Error]\033[0m"
    Blocked = " \033[91m[Blocked]\033[0m"
    BadRequest = " \033[91m[BadRequest]\033[0m"
    UserFailed = " \033[91m[UserFailed]\033[0m"
    Callback = " \033[92m[Callback]\033[0m"
    Document = " \033[92m[Document]\033[0m"
    ToAllRegistered = " \033[92m[ToAllRegistered]\033[0m"
    Pending = " \033[96m[Pending]\033[0m"
    ZeroMessage = " \033[96m[ZeroMessage]\033[0m"
    NoText = " \033[96m[NoText]\033[0m"


class MsgIO(str, Enum):
    In = "\033[35m>>\033[0m"
    Out = "\033[36m<<\033[0m"


async def SendDocument(
    chat_id: int,
    document: types.FSInputFile,
    caption: str | None = None,
) -> types.Message | None:
    addendum = MsgContext.No

    message: types.Message | None = None
    try:
        message = await bot.send_document(
            chat_id=chat_id,
            document=document,
            caption=caption,
        )

        ctx = await user_ctx()
        await ctx.RegisterOutgoingMessage(message)

    except TelegramForbiddenError:
        addendum = MsgContext.Blocked

    except TelegramBadRequest:
        addendum = MsgContext.BadRequest

    username = await GetChatTgUsername(chat_id) or "-/-"
    logging.info(
        f"chat_id={chat_id:<10} ({username + ")":<25} {MsgIO.Out.value}{addendum.value}{MsgContext.Document.value} {caption}"
    )

    return message


async def SendMessage(
    chat_id: int,
    text: str,
    reply_markup: (
        types.ReplyKeyboardMarkup
        | types.ReplyKeyboardRemove
        | types.InlineKeyboardMarkup
        | None
    ) = None,
    context: MsgContext = MsgContext.No,
) -> types.Message | None:
    addendum = MsgContext.No

    message: types.Message | None = None
    try:
        message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
        )

        ctx = await user_ctx()
        await ctx.RegisterOutgoingMessage(message)
    except TelegramForbiddenError:
        addendum = MsgContext.Blocked
        # TODO: make his matching inactive & but DON'T make him unverified
    except TelegramBadRequest:
        addendum = MsgContext.BadRequest

    username = await GetChatTgUsername(chat_id) or "-/-"
    logging.info(
        f"chat_id={chat_id:<10} ({username + ")":<25} {MsgIO.Out.value}{addendum.value}{context.value} {repr(text)}"
    )

    return message


@dataclass
class PersonalMsg:
    chat_id: int
    text: str


async def SendMessagesToGroup(messages: list[PersonalMsg]) -> None:
    limiter = AsyncLimiter(max_rate=30, time_period=1)

    async def SendMessageLimited(message: PersonalMsg) -> None:
        nonlocal limiter

        async with limiter:
            await SendMessage(
                chat_id=message.chat_id,
                text=message.text,
                context=MsgContext.ToAllRegistered,
            )

    tasks = []
    for message in messages:
        tasks.append(SendMessageLimited(message))

    await asyncio.gather(*tasks)


async def ReceiveMessage(
    message: types.Message,
    context: MsgContext = MsgContext.No,
) -> None:
    chat_id = message.chat.id

    async def CheckNewUser() -> None:
        nonlocal message, chat_id

        ctx = await user_ctx()
        exists = await ctx.CheckTgUserExists(chat_id)

        if exists:
            return

        if message.from_user is None:
            await ctx.RegisterTgUser(chat_id=chat_id)
            return

        await ctx.RegisterTgUser(
            chat_id=chat_id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
        )

    await CheckNewUser()

    username = await GetChatTgUsername(chat_id) or "-/-"
    logging.info(
        f"chat_id={chat_id:<10} ({username + ")":<25} {MsgIO.In.value}{context.value} {repr(message.text)}"
    )

    ctx = await user_ctx()
    await ctx.RegisterIncomingMessage(message)


async def ReceiveCallback(
    callback_query: types.CallbackQuery,
    callback_data: CallbackData,
    context: MsgContext = MsgContext.No,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    chat_id = callback_query.message.chat.id
    prefix = f"Callback: {callback_data.__prefix__}"
    dump = f"model_dump={callback_data.model_dump()}"

    username = await GetChatTgUsername(chat_id) or "-/-"
    logging.info(
        f"chat_id={chat_id:<10} ({username + ")":<25} {MsgIO.In.value}{MsgContext.Callback.value}{context.value} {prefix}"
    )
    logging.debug(f"chat_id={chat_id:<10}, {dump}")
