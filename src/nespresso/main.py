import asyncio

from nespresso.bot.creator import bot, dp
from nespresso.bot.handlers.common.register import (
    RegisterHandlerCancel,
    RegisterHandlerZeroMessage,
)
from nespresso.bot.lib.notifications.admin import NotifyOnShutdown, NotifyOnStartup
from nespresso.bot.lib.notifications.erroring import error_handling
from nespresso.bot.lib.notifications.pending import ProcessPendingUpdates
from nespresso.core import logs

# from handlers.admin import admin
# from handlers.client import client
# from handlers.client.menu import set_commands


async def OnStartup() -> None:
    await logs.LoggerStart()
    await NotifyOnStartup()
    await ProcessPendingUpdates()


async def OnShutdown() -> None:
    await NotifyOnShutdown()
    await logs.LoggerShutdown()


@error_handling
async def main() -> None:
    """
    Registers handlers, sets commands, and starts polling for updates.
    """
    try:
        RegisterHandlerZeroMessage(dp)
        # admin.register_handlers_admin(dp)
        # client.register_handlers_client(dp)
        RegisterHandlerCancel(dp)

        dp.startup.register(OnStartup)
        dp.shutdown.register(OnShutdown)

        # await set_commands(bot)

        await dp.start_polling(bot, drop_pending_updates=True)
    finally:
        pass


if __name__ == "__main__":
    asyncio.run(main())

# now you can run:
# $ python -m nespresso
