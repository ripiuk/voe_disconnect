import datetime
from typing import Iterable

import lxml.html as lh

from voe.utils import batcher
from voe.models import DayInfo


def parse_queue_number(html_fragment: str) -> float | None:
    """Get queue number from HTML fragment"""
    doc = lh.fromstring(html_fragment)
    disconnection_detailed_table = doc.find_class('disconnection-detailed-table')[0]
    try:
        queue_number: str = disconnection_detailed_table.xpath('//p')[0].text_content()
        queue_number = queue_number.replace('черга', '').strip()
        return float(queue_number)
    except (IndexError, AttributeError, ValueError) as err:
        # TODO: replace with logging
        print(f'Can not parse the queue number. {err.__class__.__name__}: {err}')
        return None


def parse_days_info(html_fragment: str) -> list[DayInfo]:
    """Parse response data and generate disconnection days info

    :param html_fragment: A fragment of the HTML response
    :return: A list of DayInfo objects
    """
    # TODO: handle errors
    doc = lh.fromstring(html_fragment)
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

    days_info = [
        DayInfo(
            day=day,
            disconnection_hours=[
                datetime.datetime.strptime(hour, '%H:%M').time()
                for hour, has_disconnection in list(zip(hours, batch))
                if has_disconnection
            ]
        )
        for day, batch in zip(days, batcher(has_disconnection_info, batch_size=len(hours)))
    ]
    return days_info
