import datetime
from typing import Literal

from pydantic import BaseModel, constr, conint


class InsertCommand(BaseModel):
    command: Literal['insert']
    data: constr(min_length=100)


class DayInfo(BaseModel):
    day: constr(min_length=1)
    disconnection_hours: list[datetime.time] = []


class QueueInfo(BaseModel):
    name: constr(min_length=1)
    number: float | None = None
    raw_data: constr(min_length=100)
    days: list[DayInfo] = []

    class Config:
        validate_assignment = True


class VOESearchParams(BaseModel):
    title: str
    city_id: conint(ge=0)
    street_id: conint(ge=0)
    house_id: conint(ge=0)


class TimeRange(BaseModel):
    start: datetime.time
    end: datetime.time | None = None

    @classmethod
    def with_incremented_end_hour(cls, start: datetime.time, end: datetime.time | None) -> 'TimeRange':
        """Create TimeRange object, increment the end time by 1 hour"""
        return TimeRange(
            start=start,
            end=(
                datetime.time(hour=0 if end.hour == 23 else end.hour + 1, minute=end.minute)
                if end and start != end
                else None
            )
        )
