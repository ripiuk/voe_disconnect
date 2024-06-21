from voe.models import DayInfo


def day_info_into_telegram_markdown_v2(days_info: list[DayInfo]) -> str:
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
    message = message.replace('.', r'\.').replace('-', r'\-')
    return message
