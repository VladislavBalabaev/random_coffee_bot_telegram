import logging

from aiogram import types
from aiogram.exceptions import TelegramForbiddenError

from nespresso.bot.creator import bot
from nespresso.core.services import user_ctx

_BLOCKED: str = " \033[91m[Blocked]\033[0m"
_FAIL: str = " \033[91m[Fail]\033[0m"
_PENDING: str = " \033[91m[Pending]\033[0m"
_ZERO_MESSAGE: str = " \033[91m[ZeroMessage]\033[0m"


async def SendMessage(
    chat_id: int,
    text: str,
    reply_markup: types.ReplyKeyboardMarkup | types.ReplyKeyboardRemove | None = None,
    on_fail: bool = False,
) -> None:
    """
    Sends a message to the user, logs it, and updates the message history in DB.
    Accounts for blocking by user.
    """
    ctx = await user_ctx

    try:
        await bot.send_message(chat_id, text, reply_markup=reply_markup)

        await ctx.RegisterOutgoingMessage(chat_id, text)

        blocked = ""
    except TelegramForbiddenError:
        blocked = _BLOCKED

    username = await ctx.GetTgUsername(chat_id)
    fail = _FAIL if on_fail else ""
    logging.info(
        f"chat_id={chat_id:<10} ({username:<25}) \033[36m<<\033[0m{blocked}{fail} {repr(text)}"
    )


async def ReceiveMessage(
    message: types.Message, on_pending: bool = False, on_zero_message: bool = False
) -> None:
    """
    Logs the incoming message, and updates the message history in DB.
    """

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
            chat_id=message.chat.id, text="Бот определяет только текст", on_fail=True
        )

    text = str(message.text)
    chat_id = message.chat.id

    ctx = await user_ctx

    await ctx.RegisterIncomingMessage(chat_id, text)

    username = await ctx.GetTgUsername(chat_id)
    pending = _PENDING if on_pending else ""
    zm = _ZERO_MESSAGE if on_zero_message else ""

    logging.info(
        f"chat_id={chat_id:<10} ({username:<25}) \033[35m>>\033[0m{pending}{zm} {repr(message.text)}"
    )

    await CheckNewUser(message)
    await CheckText(message)
