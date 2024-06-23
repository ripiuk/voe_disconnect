from typing import Iterator

from voe.models import QueueInfo, DayInfo


def _day_info_into_telegram_markdown_v2(days_info: list[DayInfo]) -> str:
    """Convert disconnection days info into telegram MarkdownV2 format

    :param days_info: List of disconnection days info
    :return: telegram MarkdownV2 formatted days info
    """
    message = '\n'.join(
        f'*{day_info.day}* - Відсутнє світло о *{
            ", ".join(disconnection_hour for disconnection_hour in day_info.disconnection_hours)
        }*'
        for day_info in days_info
        if day_info.disconnection_hours
    )

    return message or 'Відключень не заплановано'


def convert_into_telegram_markdown_v2(lines_info: Iterator[QueueInfo]) -> str:
    """Convert queue info into telegram MarkdownV2 format

    :param lines_info: List of disconnection queues info
    :return: telegram MarkdownV2 formatted queues info
    """
    message = '\n\n'.join(
        f'*{line_info.name}*\n{_day_info_into_telegram_markdown_v2(line_info.days)}'
        for line_info in lines_info
    )
    message = message.replace('.', r'\.').replace('-', r'\-').replace('(', r'\(').replace(')', r'\)')

    return message
