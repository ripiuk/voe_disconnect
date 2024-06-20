import requests

from config import Settings


settings = Settings()


def send_telegram_message(message: str) -> None:
    """Send telegram message to a specified chat id
    :param message: message to send
    :return: None
    :raises ValueError: if message can not be sent to the chat id
    """
    # TODO: add retries, handle errors
    response = requests.get(
        url=f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage',
        params={
            'chat_id': settings.TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'MarkdownV2',
        },
    )
    response.raise_for_status()
    if not response.json()['ok'] is True:
        raise ValueError('Failed to send a telegram message')


if __name__ == '__main__':
    send_telegram_message('Hey from *GitHub Actions*')
