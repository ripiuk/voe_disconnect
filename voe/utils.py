from typing import Iterable
from itertools import islice


def batcher(iterable: Iterable, *, batch_size: int) -> Iterable[list]:
    """Splits an iterable into batches

    :param iterable: The iterable to split
    :param batch_size: The size of the batch
    :return: An iterable of batches
    """
    iterator = iter(iterable)
    while batch := list(islice(iterator, batch_size)):
        yield batch
