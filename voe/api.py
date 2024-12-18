import logging
from concurrent.futures import ThreadPoolExecutor

import requests
from requests import Session
from pydantic import ValidationError
from requests.exceptions import HTTPError, RequestException, Timeout, ConnectionError, ProxyError

from voe.utils import retry
from voe.models import QueueInfo, VOESearchParams, InsertCommand


logger = logging.getLogger('voe.api')


def _get_proxy_info() -> dict:
    """Get proxy info for voe requests"""
    resp = requests.get('https://gimmeproxy.com/api/getProxy?post=true&supportsHttps=true&protocol=http').json()
    ip_info = resp['ipPort']

    return {
        'http': ip_info,
        'https': ip_info,
    }


@retry(
    max_retries=10,
    sleep_time_sec=1,
    exceptions=(HTTPError, RequestException, Timeout, ConnectionError, ProxyError),
)
def _initialize_session() -> Session:
    """Initialize requests session, grab cookies"""
    session = Session()
    session.proxies.update(_get_proxy_info())
    # HEAD requests to grab the session cookie
    response = session.head(
        url='https://www.voe.com.ua/disconnection/detailed',
        headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,uk-UA;q=0.8,uk;q=0.7',
            'Priority': 'u=1, i',
            'Connection': 'keep-alive',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        },
    )
    logger.info(f'HEAD response status code: {response.status_code}')
    response.raise_for_status()
    return session


@retry(max_retries=4, sleep_time_sec=1, exceptions=(HTTPError, RequestException, Timeout, ConnectionError))
def _get_queue_info(*, session: Session, search_params: VOESearchParams) -> QueueInfo:
    """Make a VOE API request and search for needed data

    :param session: Requests session
    :param search_params: VOE search parameters
    :return: QueueInfo object
    """
    response = session.post(
        url='https://www.voe.com.ua/disconnection/detailed?ajax_form=1',
        params={'_wrapper_format': 'drupal_ajax'},
        data={
            'search_type': '0',
            'city_id': search_params.city_id,
            'street_id': search_params.street_id,
            'house_id': search_params.house_id,
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
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        }
    )
    logger.info(
        f'VOE API response status code: {response.status_code} '
        f'(for the {search_params.title!r} queue)'
    )
    response.raise_for_status()

    response_data = response.json()
    if not isinstance(response_data, list):
        raise ValueError(f'Got unexpected response data type: {response_data!r}')

    for item in response_data:
        try:
            insert_command = InsertCommand.model_validate(item)
            return QueueInfo(
                name=search_params.title,
                raw_data=insert_command.data,
            )
        except ValidationError:
            continue

    raise ValueError(f'Con not find any insert command in the response: {response_data!r}')


def execute_all_search_params(
    voe_search_params: list[VOESearchParams],
    *,
    max_workers_num: int = 3,
) -> list[QueueInfo]:
    """Get queues info from the VOE website based on search params

    :param voe_search_params: VOE search parameters
    :param max_workers_num: Maximum number of concurrent requests
    :return: list of QueueInfo objects
    """
    session = _initialize_session()
    with ThreadPoolExecutor(max_workers=max_workers_num) as executor:  # TODO: use httpx or aiohttp instead
        queues_info = list(
            executor.map(
                lambda search_params: _get_queue_info(
                    session=session,
                    search_params=search_params
                ),
                voe_search_params,
            )
        )
    return queues_info
