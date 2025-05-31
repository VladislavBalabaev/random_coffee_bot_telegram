import logging
from collections.abc import Awaitable, Callable
from logging.handlers import QueueListener


async def LoggerStart(setup: Callable[[], Awaitable[QueueListener]]) -> None:
    listener = await setup()
    listener.start()

    logging.info("# Logging started.")


async def LoggerShutdown() -> None:
    logging.info("# Logging stopped.")

    logging.shutdown()
