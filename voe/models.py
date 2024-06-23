from typing import Literal

from pydantic import BaseModel, constr


class InsertCommand(BaseModel):
    command: Literal['insert']
    data: constr(min_length=100)


class DayInfo(BaseModel):
    day: constr(min_length=1)
    disconnection_hours: list[str] = []


class QueueInfo(BaseModel):
    name: constr(min_length=1)
    days: list[DayInfo]
