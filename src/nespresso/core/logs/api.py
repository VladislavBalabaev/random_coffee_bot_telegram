import logging
from logging.handlers import QueueListener

from nespresso.core.configs.paths import PATH_API_LOGS
from nespresso.core.logs.settings import (
    CreateConsoleHandler,
    CreateFileHandler,
    CreateListener,
)

_LOGGING_LISTENER: QueueListener


async def LoggerSetup() -> None:
    global _LOGGING_LISTENER  # noqa: PLW0603

    # ─── SQLAlchemy settings ───
    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.setLevel(logging.WARNING)

    console_handler = CreateConsoleHandler(logging.INFO)
    bot_file_handler = CreateFileHandler(PATH_API_LOGS, logging.INFO)

    # ─── Queue ───
    _LOGGING_LISTENER = CreateListener(console_handler, bot_file_handler)


async def LoggerStart() -> None:
    await LoggerSetup()

    _LOGGING_LISTENER.start()
    logging.info("# Logging started.")


async def LoggerShutdown() -> None:
    logging.info("# Logging stopped.")
    _LOGGING_LISTENER.stop()
    logging.shutdown()
