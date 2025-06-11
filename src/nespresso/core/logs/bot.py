import logging
from logging.handlers import QueueListener

from nespresso.core.configs.paths import PATH_BOT_LOGS
from nespresso.core.logs.settings import (
    CreateConsoleHandler,
    CreateFileHandler,
    CreateListener,
    FilterOutLogs,
)


async def LoggerSetup() -> QueueListener:
    console_handler = CreateConsoleHandler(
        logging.INFO,
        filters=[
            FilterOutLogs("sqlalchemy.engine", logging.WARNING),
            FilterOutLogs("aiogram", logging.WARNING),
            FilterOutLogs("opensearch", logging.WARNING),
            FilterOutLogs("apscheduler.scheduler", logging.WARNING),
        ],
    )
    bot_file_handler = CreateFileHandler(
        PATH_BOT_LOGS,
        logging.DEBUG,
    )

    listener: QueueListener = CreateListener(console_handler, bot_file_handler)

    return listener
