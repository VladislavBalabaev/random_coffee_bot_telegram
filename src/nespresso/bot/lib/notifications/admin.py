import logging

from aiogram import types

from nespresso.bot.lib.messaging.stream import SendDocument, SendMessage
from nespresso.core.configs.paths import PATH_LOGS
from nespresso.core.constants import ADMIN_CHAT_IDS


async def NotifyOnStartup() -> None:
    logging.info("# Bot started.")

    for admin in ADMIN_CHAT_IDS:
        await SendMessage(chat_id=admin, text="# Bot started.")


async def NotifyOnShutdown() -> None:
    for admin in ADMIN_CHAT_IDS:
        await SendDocument(
            chat_id=admin,
            document=types.FSInputFile(PATH_LOGS),
            caption="# Bot stopped.",
        )

    logging.info("# Logging stopped.")
