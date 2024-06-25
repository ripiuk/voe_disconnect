from voe.utils import combine_hours
from voe.models import QueueInfo, DayInfo


def _day_info_into_telegram_markdown_v2(days_info: list[DayInfo]) -> str:
    """Convert disconnection days info into telegram MarkdownV2 format

    :param days_info: List of disconnection days info
    :return: telegram MarkdownV2 formatted days info
    """
    message = '\n'.join(
        f'*{day_info.day}* - Відсутнє світло о *{
            ", ".join(
                (
                    time_range.start.strftime('%H:%M') 
                    if time_range.end is None 
                    else f'{time_range.start.strftime('%H:%M')}-{time_range.end.strftime('%H:%M')}'
                ) 
                for time_range in combine_hours(day_info.disconnection_hours)
            )
        }*'
        for day_info in days_info
        if day_info.disconnection_hours
    )

    return message or 'Відключень не заплановано'


def convert_into_telegram_markdown_v2(queues_info: list[QueueInfo]) -> str:
    """Convert queue info into telegram MarkdownV2 format

    :param queues_info: List of disconnection queues info
    :return: telegram MarkdownV2 formatted queues info
    """
    message = '\n\n'.join(
        f'*{f"{queue_info.name} ({queue_info.number})" if queue_info.number else queue_info.name}*\n'
        f'{_day_info_into_telegram_markdown_v2(queue_info.days)}'
        for queue_info in queues_info
    )
    message = message.replace('.', r'\.').replace('-', r'\-').replace('(', r'\(').replace(')', r'\)')

    return message
