import logging
from logging.handlers import QueueListener

from nespresso.core.configs.paths import PATH_API_LOGS
from nespresso.core.logs.settings import (
    CreateConsoleHandler,
    CreateFileHandler,
    CreateListener,
)

LISTENER: QueueListener


async def LoggerSetup() -> None:
    global LISTENER  # noqa: PLW0603

    # ─── SQLAlchemy settings ───
    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.setLevel(logging.WARNING)

    console_handler = CreateConsoleHandler(logging.INFO)
    bot_file_handler = CreateFileHandler(PATH_API_LOGS, logging.INFO)

    # ─── Queue ───
    LISTENER = CreateListener(console_handler, bot_file_handler)
