import asyncio
import logging
from enum import Enum

from aiogram import types
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters.callback_data import CallbackData
from aiolimiter import AsyncLimiter

from nespresso.bot.lib.chat.username import GetChatTgUsername
from nespresso.bot.lifecycle.creator import bot
from nespresso.db.services.user_context import user_ctx


class MessageContext(str, Enum):
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


class MessageIO(str, Enum):
    In = "\033[35m>>\033[0m"
    Out = "\033[36m<<\033[0m"


async def SendDocument(
    chat_id: int,
    document: types.FSInputFile,
    caption: str | None = None,
) -> types.Message | None:
    addendum = MessageContext.No

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
        addendum = MessageContext.Blocked

    except TelegramBadRequest:
        addendum = MessageContext.BadRequest

    username = await GetChatTgUsername(chat_id)
    logging.info(
        f"chat_id={chat_id:<10} ({username:<25}) {MessageIO.Out.value}{addendum.value}{MessageContext.Document.value} {caption}"
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
    context: MessageContext = MessageContext.No,
) -> types.Message | None:
    addendum = MessageContext.No

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
        addendum = MessageContext.Blocked
    except TelegramBadRequest:
        addendum = MessageContext.BadRequest

    username = await GetChatTgUsername(chat_id)
    logging.info(
        f"chat_id={chat_id:<10} ({username:<25}) {MessageIO.Out.value}{addendum.value}{context.value} {text}"
    )

    return message


async def SendMessageToGroup(chat_ids: list[int], text: str) -> None:
    limiter = AsyncLimiter(max_rate=30, time_period=1)

    async def SendMessageLimited(chat_id: int, text: str) -> None:
        nonlocal limiter

        async with limiter:
            await SendMessage(
                chat_id=chat_id,
                text=text,
                context=MessageContext.ToAllRegistered,
            )

    tasks = []
    for chat_id in chat_ids:
        tasks.append(SendMessageLimited(chat_id=chat_id, text=text))

    await asyncio.gather(*tasks)


async def ReceiveMessage(
    message: types.Message,
    context: MessageContext = MessageContext.No,
) -> None:
    async def CheckNewUser(message: types.Message) -> None:
        ctx = await user_ctx()

        exists = await ctx.CheckTgUserExists(message.chat.id)

        if not exists:
            if message.from_user is not None:
                await ctx.RegisterTgUser(
                    chat_id=message.chat.id,
                    username=message.from_user.username,
                    full_name=message.from_user.full_name,
                )
            else:
                await ctx.RegisterTgUser(chat_id=message.chat.id)

    await CheckNewUser(message)

    chat_id = message.chat.id

    username = await GetChatTgUsername(chat_id)
    logging.info(
        f"chat_id={chat_id:<10} ({username:<25}) {MessageIO.In.value}{context.value} {message.text}"
    )

    ctx = await user_ctx()
    await ctx.RegisterIncomingMessage(message)


async def ReceiveCallback(
    callback_query: types.CallbackQuery,
    callback_data: CallbackData,
    context: MessageContext = MessageContext.No,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    chat_id = callback_query.message.chat.id
    prefix = f"Callback: {callback_data.__prefix__}"
    dump = f"model_dump={callback_data.model_dump()}"

    username = await GetChatTgUsername(chat_id)
    logging.info(
        f"chat_id={chat_id:<10} ({username:<25}) {MessageIO.In.value}{MessageContext.Callback.value}{context.value} {prefix}"
    )
    logging.debug(f"chat_id={chat_id:<10}, {dump}")
