import logging
import re
from logging import StreamHandler
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from pathlib import Path
from queue import Queue
from typing import Any

from colorlog import ColoredFormatter
from pythonjsonlogger.json import JsonFormatter

_CONSOLE_FORMAT = ColoredFormatter(
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


_FILE_FORMAT = JsonFormatter(
    fmt="%(levelname)s %(asctime)s %(message)s %(name)s %(filename)s %(lineno)d",
    json_ensure_ascii=False,
)


class EscapeNewlinesFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = record.getMessage().replace("\n", "\\n")
        return True


class AiogramFilter(logging.Filter):
    def __init__(self, level: int = 100):  # 100 - block of any logs
        super().__init__()

        self.level = level

    def filter(self, record: logging.LogRecord) -> bool:
        return not (record.levelno < self.level and record.name.startswith("aiogram"))


class RemoveColorCodesFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = self.RemoveColorCodes(str(record.msg))
        return True

    @staticmethod
    def RemoveColorCodes(text: str) -> str:
        return re.sub(r"\x1b\[[0-9;]*m", "", text)


def CreateFileHandler(
    path: Path, level: int, filters: list[logging.Filter] | None = None
) -> RotatingFileHandler:
    handler = RotatingFileHandler(  # 3 GB
        path,
        maxBytes=256 * 1024 * 1024,
        backupCount=12,
        encoding="utf-8",
    )
    handler.setLevel(level)
    handler.setFormatter(_FILE_FORMAT)

    handler.addFilter(RemoveColorCodesFilter())

    if filters:
        for filt in filters:
            handler.addFilter(filt)

    return handler


def CreateConsoleHandler(
    level: int, filters: list[logging.Filter] | None = None
) -> StreamHandler[Any]:
    handler = StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(_CONSOLE_FORMAT)

    handler.addFilter(EscapeNewlinesFilter())

    if filters:
        for filt in filters:
            handler.addFilter(filt)

    return handler


def CreateListener(*handlers: logging.Handler) -> QueueListener:
    que: Queue[Any] = Queue()

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(QueueHandler(que))

    listener = QueueListener(que, *handlers, respect_handler_level=True)

    return listener
