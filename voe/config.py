from pathlib import Path
from enum import StrEnum, unique

from pydantic import constr
from pydantic_settings import BaseSettings, SettingsConfigDict

from voe.models import VOESearchParams


@unique
class LogLevels(StrEnum):
    CRITICAL = 'CRITICAL'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    DEBUG = 'DEBUG'
    NOTSET = 'NOTSET'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / '.env',
        env_file_encoding='utf-8',
    )

    LOG_LEVEL: LogLevels = LogLevels.INFO
    LOG_ROOT_LEVEL: LogLevels = LogLevels.WARNING

    TELEGRAM_TOKEN: constr(min_length=1)
    TELEGRAM_CHAT_ID: constr(min_length=1)

    SEARCH_PARAMS: list[VOESearchParams]
