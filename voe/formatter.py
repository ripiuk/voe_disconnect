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
        }* ({_get_total_hours_amount_label(day_info.disconnection_hours)})'
        for day_info in days_info
        if day_info.disconnection_hours
    )

    return message or 'Відключень не заплановано'


def _get_total_hours_amount_label(disconnection_hours: list) -> str:
    """Get the total hours amount label with correct numeral ending"""
    amount = len(disconnection_hours)
    tens, ones = amount // 10 % 10, amount % 10

    match (tens, ones):
        case (1, _):
            # 10,11,12,13,14,15,16,17,18,19,110,111,...
            hour_label = 'годин'
        case (_, 1):
            # 1,21,31,41,...
            hour_label = 'година'
        case (_, 2) | (_, 3) | (_, 4):
            # 2,3,4,22,23,24,32,33,34,...
            hour_label = 'години'
        case _:
            # 0,5,6,7,8,9,20,25,26,27,28,29,30,...
            hour_label = 'годин'

    return f'{amount} {hour_label}'


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
