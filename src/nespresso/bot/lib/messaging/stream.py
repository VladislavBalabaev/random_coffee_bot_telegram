import logging

from aiogram import types

from nespresso.bot.creator import bot
from nespresso.bot.lib.messaging.checks import new_user
from nespresso.core.services import user_ctx

_fail: str = " \033[91m[FAIL]\033[0m"


# @check_didnt_block    !!!
async def SendMessage(
    user_id: int,
    text: str,
    reply_markup: types.ReplyKeyboardMarkup | types.ReplyKeyboardRemove | None = None,
    on_fail: bool = False,
) -> None:
    """
    Sends a message to the user, logs the message, and updates the message history in MongoDB.
    """
    ctx = await user_ctx

    await ctx.AddBotMessage(user_id, text)

    await bot.send_message(user_id, text, reply_markup=reply_markup)

    username = await ctx.UsernameById(user_id)
    fail = _fail if on_fail else ""

    logging.info(f"_id={user_id:<10} {username} \033[36m<<\033[0m{fail} {repr(text)}")


@new_user
async def ReceiveMessage() -> None: ...
