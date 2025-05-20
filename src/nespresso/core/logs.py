import logging
import re
from logging import StreamHandler
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from queue import Queue
from typing import Any

from colorlog import ColoredFormatter
from pythonjsonlogger.jsonlogger import JsonFormatter  # type: ignore[attr-defined]

from nespresso.core.configs.paths import PATH_LOGS

_LOGGING_LISTENER: QueueListener


console_format = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s :: %(asctime)s.%(msecs)03d :: %(message)s",
    datefmt="%m-%d %H:%M:%S",
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)


# file_format = logging.Formatter(
#     "%(levelname)-8s :: %(name)-25s :: %(asctime)s :: %(message)s :: (%(filename)s:%(lineno)d)"
# )
file_format = JsonFormatter(
    fmt="%(levelname)s %(asctime)s %(message)s %(name)s %(filename)s %(lineno)d",
)


class AiogramFilter(logging.Filter):
    """
    Filter to block 'aiogram' INFO-level logs from being displayed in the console, but allows others.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelname == "INFO" and record.name.startswith("aiogram"):
            return False
        return True


class RemoveColorCodesFilter(logging.Filter):
    """
    Filter that removes color codes from log messages before writing them to the log file.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = self.RemoveColorCodes(str(record.msg))
        return True

    @staticmethod
    def RemoveColorCodes(text: str) -> str:
        return re.sub(r"\x1b\[[0-9;]*m", "", text)


async def LoggerSetup() -> None:
    global _LOGGING_LISTENER  # noqa: PLW0603

    que: Queue[Any] = Queue()

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(QueueHandler(que))

    aiogram_logger = logging.getLogger("aiogram")
    aiogram_logger.setLevel(logging.INFO)

    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.setLevel(logging.WARNING)

    console_handler = StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_format)
    console_handler.addFilter(AiogramFilter())

    file_handler = RotatingFileHandler(  # 3 GB
        PATH_LOGS,
        maxBytes=128 * 1024 * 1024,
        backupCount=8 * 3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_format)
    file_handler.addFilter(RemoveColorCodesFilter())

    _LOGGING_LISTENER = QueueListener(
        que, console_handler, file_handler, respect_handler_level=True
    )


async def LoggerStart() -> None:
    await LoggerSetup()

    _LOGGING_LISTENER.start()
    logging.info("# Logging started.")


async def LoggerShutdown() -> None:
    logging.info("# Logging stopped.")
    _LOGGING_LISTENER.stop()
