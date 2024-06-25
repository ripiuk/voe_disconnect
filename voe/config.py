from pathlib import Path

from pydantic import constr
from pydantic_settings import BaseSettings, SettingsConfigDict

from voe.models import VOESearchParams


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / '.env',
        env_file_encoding='utf-8',
    )

    TELEGRAM_TOKEN: constr(min_length=1)
    TELEGRAM_CHAT_ID: constr(min_length=1)

    SEARCH_PARAMS: list[VOESearchParams]
