from aiogram import Dispatcher

from nespresso.bot.handlers.admin.commands import logs, messages, send


def RegisterAdminHandlers(dp: Dispatcher) -> None:
    dp.include_routers(
        logs.router,
        messages.router,
        send.router,
    )
