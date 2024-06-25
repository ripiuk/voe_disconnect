from voe.config import Settings
from voe import api, html_parser, formatter, telegram


class Application:

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def notify_in_telegram(self) -> None:
        """Notify about VOE disconnection status in telegram"""
        queues_info = api.execute_all_search_params(voe_search_params=self.settings.SEARCH_PARAMS)
        for queue_info in queues_info:
            queue_info.number = html_parser.parse_queue_number(queue_info.raw_data)
            queue_info.days = html_parser.parse_days_info(queue_info.raw_data)

        message = formatter.convert_into_telegram_markdown_v2(queues_info)
        telegram.send_message(message, settings=self.settings)
