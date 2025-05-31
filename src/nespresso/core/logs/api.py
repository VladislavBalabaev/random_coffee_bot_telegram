import logging
from logging.handlers import QueueListener

from nespresso.core.configs.paths import PATH_API_LOGS
from nespresso.core.logs.settings import (
    CreateConsoleHandler,
    CreateFileHandler,
    CreateListener,
    FilterOutLogs,
)

LISTENER: QueueListener


async def LoggerSetup() -> None:
    global LISTENER  # noqa: PLW0603

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("opensearch").setLevel(logging.INFO)

    # ─── API Handlers ───
    console_handler = CreateConsoleHandler(
        logging.INFO,
        filters=[
            FilterOutLogs("opensearch", logging.WARNING),
        ],
    )
    bot_file_handler = CreateFileHandler(
        PATH_API_LOGS,
        logging.INFO,
    )

    # ─── Queue ───
    LISTENER = CreateListener(console_handler, bot_file_handler)
