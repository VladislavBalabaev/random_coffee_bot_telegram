from aiogram import Dispatcher

from nespresso.bot.handlers.admin.commands import (
    admin,
    blocking,
    logs,
    matching,
    messages,
    send,
    senda,
)


def RegisterAdminHandlers(dp: Dispatcher) -> None:
    dp.include_routers(
        admin.router,
        logs.router,
        messages.router,
        send.router,
        senda.router,
        blocking.router,
        matching.router,
    )
