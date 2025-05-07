from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from nespresso.core.configs.paths import PATH_ENV


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: SecretStr
    POSTGRES_DSN: SecretStr  # Data Source Name, e.g. postgresql+asyncpg://user:pass@localhost/dbname
    EMAIL_ADDRESS: SecretStr
    EMAIL_PASSWORD: SecretStr

    model_config = SettingsConfigDict(env_file=PATH_ENV, env_file_encoding="utf-8")


settings = Settings()
