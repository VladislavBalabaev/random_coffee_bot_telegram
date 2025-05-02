from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from nespesso.core.configs.paths import PATH_ENV


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: SecretStr
    MONGODB_USERNAME: SecretStr
    MONGODB_PASSWORD: SecretStr
    EMAIL_ADDRESS: SecretStr
    EMAIL_PASSWORD: SecretStr

    model_config = SettingsConfigDict(env_file=PATH_ENV, env_file_encoding="utf-8")


config = Settings()
