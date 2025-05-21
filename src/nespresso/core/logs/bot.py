import logging
from logging.handlers import QueueListener

from nespresso.core.configs.paths import PATH_AIOGRAM_LOGS, PATH_BOT_LOGS
from nespresso.core.logs.settings import (
    AiogramFilter,
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

    # ─── Aiogram File Handler ───
    aiogram_logger = logging.getLogger("aiogram")
    aiogram_logger.setLevel(logging.INFO)
    aiogram_file_handler = CreateFileHandler(PATH_AIOGRAM_LOGS, logging.INFO)
    aiogram_logger.addHandler(aiogram_file_handler)

    # ─── Bot Handlers ───
    console_handler = CreateConsoleHandler(
        logging.INFO, filters=[AiogramFilter(logging.WARNING)]
    )
    bot_file_handler = CreateFileHandler(
        PATH_BOT_LOGS, logging.DEBUG, filters=[AiogramFilter()]
    )

    _LOGGING_LISTENER = CreateListener(console_handler, bot_file_handler)


async def LoggerStart() -> None:
    await LoggerSetup()

    _LOGGING_LISTENER.start()
    logging.info("# Logging started.")


async def LoggerShutdown() -> None:
    logging.info("# Logging stopped.")
    _LOGGING_LISTENER.stop()
