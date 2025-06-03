import asyncio

from nespresso.bot.handlers.admin.register import RegisterAdminHandlers
from nespresso.bot.handlers.client.register import RegisterClientHandlers
from nespresso.bot.handlers.common.register import (
    RegisterHandlerCancel,
    RegisterHandlerZeroMessage,
)
from nespresso.bot.lib.notifications import admin
from nespresso.bot.lib.notifications.erroring import SetExceptionHandlers
from nespresso.bot.lib.notifications.pending import ProcessPendingUpdates
from nespresso.bot.lifecycle.creator import bot, dp
from nespresso.bot.lifecycle.menu import SetMenu
from nespresso.core.configs.paths import EnsurePaths
from nespresso.core.logs import flow as logs
from nespresso.core.logs.bot import LoggerSetup
from nespresso.db.session import EnsureDB
from nespresso.recsys.embedding.model import EnsureEmbeddingModel
from nespresso.recsys.search.client import (
    EnsureOpenSearchIndex,
    client as opensearch_client,
)


async def EnsureDependencies() -> None:
    await EnsureDB()
    EnsureEmbeddingModel()
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
    await logs.LoggerStart(LoggerSetup)

    await EnsureDependencies()

    dp.startup.register(OnStartup)
    dp.shutdown.register(OnShutdown)

    SetExceptionHandlers()

    await dp.start_polling(bot, drop_pending_updates=True)


# $ python -m nespresso
if __name__ == "__main__":
    asyncio.run(main())
