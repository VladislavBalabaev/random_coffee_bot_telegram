from pathlib import Path

DIR_ROOT = Path(__file__).resolve().parent.parent.parent

DIR_DATA = DIR_ROOT / "data"
DIR_LOGS = DIR_ROOT / "data" / "logs"

PATH_ENV = DIR_ROOT / ".env"
PATH_LOGS = DIR_LOGS / "logs.log"


def EnsurePaths() -> None:
    DIR_DATA.mkdir(parents=True, exist_ok=True)
    DIR_LOGS.mkdir(parents=True, exist_ok=True)

    if not PATH_ENV.exists():
        raise FileNotFoundError("`.env` file not found")
