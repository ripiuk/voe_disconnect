import requests
from requests.exceptions import HTTPError, RequestException, Timeout, ConnectionError

from voe.utils import retry
from voe.config import Settings


@retry(max_retries=3, sleep_time_sec=1, exceptions=(HTTPError, RequestException, Timeout, ConnectionError))
def send_message(message: str, *, settings: Settings) -> None:
    """Send telegram message to a specified chat id

    :param message: message to send
    :param settings: project settings
    :return: None
    :raises ValueError: if message can not be sent to the chat id
    """
    response = requests.get(
        url=f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage',
        params={
            'chat_id': settings.TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'MarkdownV2',
        },
    )
    response.raise_for_status()
    if response.json()['ok'] is not True:
        raise ValueError(f'Failed to send a telegram message. Got response {response.status_code!r}')
