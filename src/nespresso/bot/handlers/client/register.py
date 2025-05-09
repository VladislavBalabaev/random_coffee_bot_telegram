from aiogram import Dispatcher

from nespresso.bot.handlers.client.commands import start


def RegisterClientHandlers(dp: Dispatcher) -> None:
    dp.include_routers(
        start.router,
    )
