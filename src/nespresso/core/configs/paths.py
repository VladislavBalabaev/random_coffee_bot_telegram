from pathlib import Path

DIR_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent

DIR_DATA = DIR_ROOT / "data"
DIR_LOGS = DIR_DATA / "logs"
DIR_TEMP = DIR_DATA / "temp"

DIR_RECSYS = DIR_ROOT / "recsysdata"
DIR_EMBEDDING = DIR_RECSYS / "embedding"
DIR_EMBEDDING_MODEL = DIR_EMBEDDING / "model"

_dirs = [DIR_DATA, DIR_LOGS, DIR_TEMP, DIR_RECSYS, DIR_EMBEDDING, DIR_EMBEDDING_MODEL]

PATH_ENV = DIR_ROOT / ".env"

PATH_BOT_LOGS = DIR_LOGS / "bot.log"
PATH_AIOGRAM_LOGS = DIR_LOGS / "aiogram.log"
PATH_API_LOGS = DIR_LOGS / "api.log"
PATH_EMBEDDING_DATA = DIR_EMBEDDING / "data.json"


def EnsurePaths() -> None:
    for directory in _dirs:
        directory.mkdir(parents=True, exist_ok=True)

    if not PATH_ENV.exists():
        raise FileNotFoundError("`.env` file not found")
