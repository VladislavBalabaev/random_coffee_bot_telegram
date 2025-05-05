import logging

from aiogram import types

from nespresso.bot.creator import bot
from nespresso.bot.lib.messaging.checks import new_user
from nespresso.core.services import user_ctx


async def SendMessage(
    user_id: int,
    text: str,
    reply_markup: types.ReplyKeyboardMarkup | types.ReplyKeyboardRemove | None = None,
    on_fail: bool = False,
) -> None:
    """
    Sends a message to the user, logs the message, and updates the message history in MongoDB.
    """
    await user_ctx.UpdateUserMessages(user_id, text)

    await bot.send_message(user_id, text, reply_markup=reply_markup)

    username = await user_ctx.UsernameById(user_id)
    fail = " \033[91m[FAIL]\033[0m" if on_fail else ""
    logging.info(f"_id={user_id:<10} {username} \033[36m<<\033[0m{fail} {repr(text)}")


@new_user
async def ReceiveMessage() -> None: ...
