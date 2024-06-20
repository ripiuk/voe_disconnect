from pydantic import constr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    TELEGRAM_TOKEN: constr(min_length=1)
    TELEGRAM_CHAT_ID: constr(min_length=1)
