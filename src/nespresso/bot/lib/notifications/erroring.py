import asyncio
import logging
from typing import Any

from aiogram import types
from aiogram.types.error_event import ErrorEvent

from nespresso.bot.creator import dp
from nespresso.bot.lib.messaging.stream import SendDocument
from nespresso.core.configs.constants import ADMIN_CHAT_IDS
from nespresso.core.configs.paths import PATH_BOT_LOGS


async def NotifyAdminsOfError(exc: BaseException) -> None:
    for admin in ADMIN_CHAT_IDS:
        await SendDocument(
            chat_id=admin,
            document=types.FSInputFile(PATH_BOT_LOGS),
            caption=f"🚨 Error: {exc}.\n\nCheck logs for details.",
        )


def AsyncioExceptionHandler(
    loop: asyncio.AbstractEventLoop, context: dict[str, Any]
) -> None:
    exc = context.get("exception") or RuntimeError(context.get("message"))

    loop.create_task(NotifyAdminsOfError(exc))
    loop.default_exception_handler(context)  # default: do own handling


@dp.error()
async def AiogramExceptionHandler(event: ErrorEvent) -> bool:
    logging.exception(
        f"Cause exception while processing update:\n{event.model_dump()}",
        exc_info=event.exception,
    )

    await NotifyAdminsOfError(event.exception)

    return True


def SetExceptionHandlers() -> None:
    asyncio.get_running_loop().set_exception_handler(AsyncioExceptionHandler)
