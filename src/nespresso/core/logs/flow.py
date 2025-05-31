import logging
from collections.abc import Awaitable, Callable
from logging.handlers import QueueListener


async def LoggerStart(
    setup: Callable[[], Awaitable[None]], listener: QueueListener
) -> None:
    await setup()
    listener.start()

    logging.info("# Logging started.")


async def LoggerShutdown(listener: QueueListener) -> None:
    logging.info("# Logging stopped.")

    listener.stop()
    logging.shutdown()
