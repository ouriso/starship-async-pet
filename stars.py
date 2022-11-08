import curses
from random import choice, randint

from config import BASE_DELAY
from utils.sleep import Sleep

stars_symbols = ['*', ':', '.', '+']
stars_stages = (
    (BASE_DELAY, curses.A_DIM),
    (3 * BASE_DELAY, None),
    (5 * BASE_DELAY, curses.A_BOLD),
    (2 * BASE_DELAY, None)
)


async def star(canvas, row, column, delay, symbol='*'):
    # delay before appearance
    await Sleep(delay)
    while True:
        for ticks, style in stars_stages:
            canvas.addstr(row, column, symbol, style or curses.A_NORMAL)
            await Sleep(ticks)


def generate_stars(max_y: int, max_x: int, stars_number: int = 50) -> set:
    stars = set()
    for _ in range(stars_number):
        stars.add(
            (randint(1, max_y - 2), randint(1, max_x - 2),
             choice(stars_symbols))
        )
    return stars
