import logging
from enum import Enum

from aiogram import types
from aiogram.exceptions import TelegramForbiddenError

from nespresso.bot.creator import bot
from nespresso.core.services import user_ctx


class MessageContext(Enum):
    No = ""
    Blocked = " \033[91m[Blocked]\033[0m"
    NoText = " \033[90m[NoText]\033[0m"
    Fail = " \033[91m[Fail]\033[0m"
    Pending = " \033[90m[Pending]\033[0m"
    ZeroMessage = " \033[90m[ZeroMessage]\033[0m"
    Document = " \033[92m[Document]\033[0m"


class MessageIO(Enum):
    In = "\033[36m<<\033[0m"
    Out = "\033[35m>>\033[0m"


async def SendDocument(
    chat_id: int,
    document: types.FSInputFile,
    caption: str | None = None,
) -> None:
    ctx = await user_ctx

    try:
        await bot.send_document(chat_id=chat_id, document=document, caption=caption)

        await ctx.RegisterOutgoingMessage(chat_id, f"[Document] {caption}")

        blocked = ""
    except TelegramForbiddenError:
        blocked = MessageContext.Blocked.value

    username = await ctx.GetTgUsername(chat_id)
    logging.info(
        f"chat_id={chat_id:<10} ({username:<25}) {MessageIO.Out}{blocked}{MessageContext.Document.value} {caption}"
    )


async def SendMessage(
    chat_id: int,
    text: str,
    reply_markup: types.ReplyKeyboardMarkup | types.ReplyKeyboardRemove | None = None,
    context: MessageContext = MessageContext.No,
) -> None:
    ctx = await user_ctx

    try:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

        await ctx.RegisterOutgoingMessage(chat_id, text)

        blocked = ""
    except TelegramForbiddenError:
        blocked = MessageContext.Blocked.value

    username = await ctx.GetTgUsername(chat_id)
    logging.info(
        f"chat_id={chat_id:<10} ({username:<25}) {MessageIO.Out}{blocked}{context.value} {repr(text)}"
    )


async def ReceiveMessage(
    message: types.Message,
    context: MessageContext = MessageContext.No,
) -> None:
    async def CheckNewUser(message: types.Message) -> None:
        ctx = await user_ctx

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

    async def CheckText(message: types.Message) -> None:
        if message.text is not None:
            return

        await SendMessage(
            chat_id=message.chat.id,
            text="Бот определяет только текст",
            context=MessageContext.NoText,
        )

    text = str(message.text)
    chat_id = message.chat.id

    ctx = await user_ctx

    await ctx.RegisterIncomingMessage(chat_id, text)

    username = await ctx.GetTgUsername(chat_id)

    logging.info(
        f"chat_id={chat_id:<10} ({username:<25}) {MessageIO.In}{context.value} {repr(message.text)}"
    )

    await CheckNewUser(message)
    await CheckText(message)
