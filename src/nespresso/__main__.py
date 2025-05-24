import asyncio

from nespresso.bot.creator import bot, dp
from nespresso.bot.handlers.admin.register import RegisterAdminHandlers
from nespresso.bot.handlers.client.register import RegisterClientHandlers
from nespresso.bot.handlers.common.register import (
    RegisterHandlerCancel,
    RegisterHandlerZeroMessage,
)
from nespresso.bot.lib.notifications import admin
from nespresso.bot.lib.notifications.erroring import SetExceptionHandlers
from nespresso.bot.lib.notifications.pending import ProcessPendingUpdates
from nespresso.bot.menu import SetMenu
from nespresso.core.configs.paths import EnsurePaths
from nespresso.core.logs import bot as logs
from nespresso.db.session import InitDB


async def OnStartup() -> None:
    await InitDB()
    await SetMenu()
    EnsurePaths()

    await logs.LoggerStart()
    await admin.NotifyOnStartup()
    await ProcessPendingUpdates()


async def OnShutdown() -> None:
    await admin.NotifyOnShutdown()
    await logs.LoggerShutdown()


async def main() -> None:
    SetExceptionHandlers()

    RegisterHandlerCancel(dp)
    RegisterAdminHandlers(dp)
    RegisterClientHandlers(dp)
    RegisterHandlerZeroMessage(dp)

    dp.startup.register(OnStartup)
    dp.shutdown.register(OnShutdown)

    # await set_commands(bot)

    await dp.start_polling(bot, drop_pending_updates=True)


# $ python -m nespresso
if __name__ == "__main__":

    asyncio.run(main())
