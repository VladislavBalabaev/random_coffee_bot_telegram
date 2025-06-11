from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, Dispatcher
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, Message

from nespresso.bot.lib.chat.block import CheckIfBlocked
from nespresso.bot.lib.message.io import (
    ReceiveCallback,
    ReceiveMessage,
)


class MessageLoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        if await CheckIfBlocked(event.chat.id):
            return

        await ReceiveMessage(event)

        return await handler(event, data)


class CallbackLoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        if await CheckIfBlocked(event.from_user.id):
            return

        callback_data = data.get("callback_data")
        assert isinstance(callback_data, CallbackData)

        await ReceiveCallback(
            query=event,
            data=callback_data,
        )

        return await handler(event, data)


def SetBotMiddleware(dp: Dispatcher) -> None:
    dp.message.middleware(MessageLoggingMiddleware())
    dp.callback_query.middleware(CallbackLoggingMiddleware())
