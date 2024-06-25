import time
import logging
import datetime
from functools import wraps
from itertools import islice
from typing import Iterable, Callable, Type

from models import TimeRange


logger = logging.getLogger('voe.utils')


def batcher(iterable: Iterable, *, batch_size: int) -> Iterable[list]:
    """Splits an iterable into batches

    :param iterable: The iterable to split
    :param batch_size: The size of the batch
    :return: An iterable of batches

    Usage example:
        >>> list(batcher([1, 2, 3, 4, 5, 6, 7], batch_size=2))
        [[1, 2], [3, 4], [5, 6], [7]]
    """
    iterator = iter(iterable)
    while batch := list(islice(iterator, batch_size)):
        yield batch


def combine_hours(hours: list[datetime.time]) -> list[TimeRange]:
    """Combines hours list into a time range

    :param hours: The hours to combine
    :return: A list of time ranges

    Usage example:
        >>> combine_hours([
        ...     datetime.time(hour=2), datetime.time(hour=3), datetime.time(hour=4),
        ...     datetime.time(hour=12), datetime.time(hour=13), datetime.time(hour=17),
        ... ])
        [TimeRange(start=datetime.time(2, 0), end=datetime.time(5, 0)),
         TimeRange(start=datetime.time(12, 0), end=datetime.time(14, 0)),
         TimeRange(start=datetime.time(17, 0), end=None)]
    """
    if not hours:
        return []

    hours = sorted(hours)
    ranges: list[TimeRange] = []

    start_hour = end_hour = hours[0]
    for current_hour in hours[1:]:
        if current_hour.hour == end_hour.hour + 1:
            end_hour = current_hour
        else:
            ranges.append(TimeRange.with_incremented_end_hour(start=start_hour, end=end_hour))
            start_hour = end_hour = current_hour
    ranges.append(TimeRange.with_incremented_end_hour(start=start_hour, end=end_hour))

    return ranges


def retry(
    max_retries: int = 3,
    sleep_time_sec: int = 1,
    exceptions: tuple[Type[Exception], ...] | None = None,
) -> Callable:
    """Retries the wrapped function if the exceptions listed in the `exceptions` are thrown

    :param max_retries: The maximum number of retries
    :param sleep_time_sec: The sleep time in seconds
    :param exceptions: Tuple of exceptions to catch. If None - catch all exceptions
    :return: The wrapped function
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            last_err = None
            for _ in range(max_retries):
                try:
                    return f(*args, **kwargs)
                except Exception if exceptions is None else exceptions as err:
                    logger.error(
                        f'An error occurred while trying {f.__name__!r}. {err.__class__.__name__}: {err}. '
                        f'Attempt {_ + 1} / {max_retries}'
                    )
                    last_err = err
                    time.sleep(sleep_time_sec)
            if last_err:
                raise last_err
        return wrapper
    return decorator
