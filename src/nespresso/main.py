import asyncio

from nespresso.bot.creator import bot, dp
from nespresso.core import logs

# from db.connect import close_mongo_connection, setup_mongo_connection
# from handlers.admin import admin
# from handlers.admin.send_on import send_shutdown, send_startup
# from handlers.client import client
# from handlers.client.email import test_emails
# from handlers.client.menu import set_commands
# from handlers.common import common_handlers
# from handlers.common.pending import notify_users_with_pending_updates


async def OnStartUp() -> None:
    """
    Initializes logging, database connection, sends startup notifications, and handles pending updates.
    """
    await logs.LoggerStart()
    # await setup_mongo_connection()
    # await send_startup()
    # await test_emails()
    # await notify_users_with_pending_updates()


async def OnShutdown() -> None:
    """
    Sends shutdown notifications and closes the database connection.
    """
    # await send_shutdown()

    # close_mongo_connection()

    await logs.LoggerShutdown()


async def main() -> None:
    """
    Registers handlers, sets commands, and starts polling for updates.
    """
    try:
        # common_handlers.register_handler_cancel(dp)
        # admin.register_handlers_admin(dp)
        # client.register_handlers_client(dp)
        # common_handlers.register_handler_zero_message(dp)

        dp.startup.register(OnStartUp)
        dp.shutdown.register(OnShutdown)

        # await set_commands(bot)

        await dp.start_polling(bot, drop_pending_updates=True)
    finally:
        pass


if __name__ == "__main__":
    asyncio.run(main())

# now you can run:
# $ python -m nespresso
