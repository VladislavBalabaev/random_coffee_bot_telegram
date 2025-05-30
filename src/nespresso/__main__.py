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
from nespresso.db.session import EnsureDB
from nespresso.recsys.search.client import (
    EnsureOpenSearchIndex,
    client as opensearch_client,
)


async def EnsureDependencies() -> None:
    await EnsureDB()
    # ensure embedding
    await EnsureOpenSearchIndex()


async def OnStartup() -> None:
    await SetMenu()
    RegisterHandlerCancel(dp)
    RegisterAdminHandlers(dp)
    RegisterClientHandlers(dp)
    RegisterHandlerZeroMessage(dp)

    await admin.NotifyOnStartup()
    await ProcessPendingUpdates()


async def OnShutdown() -> None:
    await admin.NotifyOnShutdown()

    await opensearch_client.close()

    await logs.LoggerShutdown()


async def main() -> None:
    EnsurePaths()
    await logs.LoggerStart()

    await EnsureDependencies()

    dp.startup.register(OnStartup)
    dp.shutdown.register(OnShutdown)

    SetExceptionHandlers()

    await dp.start_polling(bot, drop_pending_updates=True)


# $ python -m nespresso
if __name__ == "__main__":
    asyncio.run(main())
