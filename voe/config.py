from pathlib import Path

from pydantic import BaseModel, constr, conint
from pydantic_settings import BaseSettings, SettingsConfigDict


class _VOESearchParams(BaseModel):
    title: str
    city_id: conint(ge=0)
    street_id: conint(ge=0)
    house_id: conint(ge=0)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / '.env',
        env_file_encoding='utf-8',
    )

    TELEGRAM_TOKEN: constr(min_length=1)
    TELEGRAM_CHAT_ID: constr(min_length=1)

    SEARCH_PARAMS: list[_VOESearchParams]
