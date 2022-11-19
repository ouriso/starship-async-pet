import asyncio

from config import BASE_DELAY


async def sleep(ticks: int = 1) -> None:
    """
    Implementation of a custom eventloop.
    :param ticks: number of ticks before coroutine exhaustion
    :return:
    """
    for _ in range(ticks):
        await asyncio.sleep(0)


def calculate_ticks_number(seconds_to_sleep: float) -> int:
    """
    Calculate the number of ticks before coroutine exhaustion.
    :param seconds_to_sleep: expected seconds to sleep
    :return: number of ticks depending on BASE_DELAY
    """
    return round(seconds_to_sleep / BASE_DELAY)
