from typing import Iterable

import lxml.html as lh

from voe.utils import batcher
from voe.models import InsertCommand, DayInfo


def parse_response_data(insert_command: InsertCommand) -> list[DayInfo]:
    """Parse the response data and return a dictionary of the parsed data

    :param insert_command: The insert command to parse
    :return: A dictionary of the parsed data
    """
    # TODO: handle errors
    doc = lh.fromstring(insert_command.data)
    disconnection_detailed_table = doc.find_class('disconnection-detailed-table')[0]

    hours: list[str] = [
        hour_div.text_content()
        for hour_div in disconnection_detailed_table.xpath(
            '//div[contains(@class, "disconnection-detailed-table-cell")][contains(@class, "head")]',
        )
    ]

    has_disconnection_info: Iterable[bool] = (
        'has_disconnection' in disconnection_div.classes
        for disconnection_div in disconnection_detailed_table.xpath(
            '//div[contains(@class, "disconnection-detailed-table-cell")]'
            '[contains(@class, "no_disconnection") or contains(@class, "has_disconnection")]',
        )
    )

    days: list[str] = [
        day_div.text_content()
        for day_div in disconnection_detailed_table.xpath(
            '//div[contains(@class, "disconnection-detailed-table-cell")][contains(@class, "legend")]'
            '[contains(@class, "day_col")]',
        )
    ]

    result: list[DayInfo] = [
        DayInfo(
            day=day,
            disconnection_hours=[
                hour
                for hour, has_disconnection in list(zip(hours, batch))
                if has_disconnection
            ]
        )
        for day, batch in zip(days, batcher(has_disconnection_info, batch_size=len(hours)))
    ]
    return result
