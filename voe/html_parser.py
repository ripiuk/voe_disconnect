from typing import Iterable

import lxml.html as lh

from voe.utils import batcher
from voe.models import InsertCommand, DayInfo, QueueInfo


def parse_response_data(insert_command: InsertCommand, queue_name: str) -> QueueInfo:
    """Parse the response data and return a dictionary of the parsed data

    :param insert_command: The insert command to parse
    :param queue_name: The queue name title
    :return: A dictionary of the parsed data
    """
    # TODO: handle errors
    doc = lh.fromstring(insert_command.data)
    disconnection_detailed_table = doc.find_class('disconnection-detailed-table')[0]

    try:
        queue_number: str = disconnection_detailed_table.xpath('//p')[0].text_content()
        queue_number = queue_number.replace('черга', '').strip()
        queue_name = f'{queue_name} ({queue_number})'
    except (IndexError, AttributeError):
        pass

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

    days_info: list[DayInfo] = [
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
    return QueueInfo(name=queue_name, days=days_info)
