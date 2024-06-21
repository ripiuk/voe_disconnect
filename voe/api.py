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
    session.head('https://www.voe.com.ua/disconnection/detailed')

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
            'Accept-Language': 'en-US,en;q=0.9,uk-UA;q=0.8,uk;q=0.7,ru;q=0.6',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.voe.com.ua',
            'Priority': 'u=1, i',
            'Referer': 'https://www.voe.com.ua/disconnection/detailed',
            'User-Agent': 'PostmanRuntime/7.39.0',
            'Connection': 'keep-alive',
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
