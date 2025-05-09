import logging
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from aiogram import types

from nespresso.bot.lib.messaging.stream import SendDocument
from nespresso.core.configs.paths import PATH_LOGS
from nespresso.core.constants import ADMIN_CHAT_IDS

P = ParamSpec("P")
R = TypeVar("R")


def error_handling(
    func: Callable[P, Coroutine[Any, Any, R]],
) -> Callable[P, Coroutine[Any, Any, R | None]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return await func(*args, **kwargs)
        except Exception as error:
            logging.exception(f"Unhandled error in {func.__name__}: {error}")

            for admin in ADMIN_CHAT_IDS:
                await SendDocument(
                    chat_id=admin,
                    document=types.FSInputFile(PATH_LOGS),
                    caption=f"🚨 Error in {func.__name__}: {repr(error)}.\n\nCheck logs for details.",
                )
            return None

    return wrapper
