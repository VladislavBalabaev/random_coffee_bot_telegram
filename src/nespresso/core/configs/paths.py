from pathlib import Path

DIR_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent

DIR_DATA = DIR_ROOT / "data"
DIR_LOGS = DIR_ROOT / "logs"

PATH_ENV = DIR_ROOT / ".env"

PATH_BOT_LOGS = DIR_LOGS / "bot.log"
PATH_AIOGRAM_LOGS = DIR_LOGS / "aiogram.log"
PATH_API_LOGS = DIR_LOGS / "api.log"


def EnsurePaths() -> None:
    DIR_DATA.mkdir(parents=True, exist_ok=True)
    DIR_LOGS.mkdir(parents=True, exist_ok=True)

    if not PATH_ENV.exists():
        raise FileNotFoundError("`.env` file not found")
