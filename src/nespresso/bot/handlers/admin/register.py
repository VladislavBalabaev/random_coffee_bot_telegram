from aiogram import Dispatcher

from nespresso.bot.handlers.admin.commands import logs, messages


def RegisterAdminHandlers(dp: Dispatcher) -> None:
    dp.include_routers(
        logs.router,
        messages.router,
    )
