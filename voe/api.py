from requests import Session
from pydantic import ValidationError

from voe.config import Settings
from voe.models import InsertCommand


def get_response(settings: Settings) -> InsertCommand:
    """Make a VOE API request and search for needed data

    :param settings: project settings
    :return: InsertCommand object
    """
    # TODO: add retries
    session = Session()
    # HEAD requests to grab the session cookie
    session.head(
        url='https://www.voe.com.ua/disconnection/detailed',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        },
    )

    response = session.post(
        url='https://www.voe.com.ua/disconnection/detailed?ajax_form=1',
        params={'_wrapper_format': 'drupal_ajax'},
        data={
            'search_type': '0',
            'city_id': settings.CITY_ID,
            'street_id': settings.STREET_ID,
            'house_id': settings.HOUSE_ID,
            'form_id': 'disconnection_detailed_search_form',
        },
        headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,uk-UA;q=0.8,uk;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.voe.com.ua',
            'Priority': 'u=1, i',
            'Referer': 'https://www.voe.com.ua/disconnection/detailed',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        }
    )
    response.raise_for_status()

    response_data = response.json()
    if not isinstance(response_data, list):
        raise ValueError(f'Got unexpected response data type: {response_data!r}')

    for item in response_data:
        try:
            return InsertCommand.model_validate(item)
        except ValidationError:
            continue

    raise ValueError(f'Con not find any insert command in the response: {response_data!r}')
