from aiogram import Dispatcher

from nespresso.bot.handlers.admin.commands import logs


def RegisterAdminHandlers(dp: Dispatcher) -> None:
    dp.include_routers(
        logs.router,
    )
