from typing import Iterator

from voe import telegram
from voe.config import Settings

from voe import api, html_parser, formatter, models


class Application:

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _queues_info(self) -> Iterator[models.QueueInfo]:
        """Get queues info from the website"""
        for search_params in self.settings.SEARCH_PARAMS:
            response = api.get_response(
                city_id=search_params.city_id,
                street_id=search_params.street_id,
                house_id=search_params.house_id,
            )
            queue_info = html_parser.parse_response_data(response, queue_name=search_params.title)
            yield queue_info

    def notify_in_telegram(self) -> None:
        """Notify about VOE disconnection status in telegram"""
        message = formatter.convert_into_telegram_markdown_v2(self._queues_info())
        telegram.send_message(message, settings=self.settings)
