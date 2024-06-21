from voe import telegram
from voe.config import Settings

from voe import api, html_parser, formatter


class Application:

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def notify_in_telegram(self) -> None:
        """Notify about VOE disconnection status in telegram"""
        response = api.get_response(self.settings)
        days_info = html_parser.parse_response_data(response)
        message = formatter.day_info_into_telegram_markdown_v2(days_info)
        telegram.send_message(message, settings=self.settings)
