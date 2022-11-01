import curses
from random import choice, randint
from utils.sleep import sleep_ticks


stars_symbols = ['*', ':', '.', '+']
stars_stages = (
    (10, curses.A_DIM),
    (3, None),
    (5, curses.A_BOLD),
    (3, None)
)


async def blink(canvas, row, column, delay, symbol='*'):
    symbol = choice(stars_symbols)
    await sleep_ticks(delay)
    while True:
        for ticks, style in stars_stages:
            await sleep_ticks(ticks)
            canvas.addstr(row, column, symbol, style or curses.A_NORMAL)


def generate_stars(max_y: int, max_x: int, stars_number: int = 50) -> set:
    stars = set()
    for _ in range(stars_number):
        stars.add(
            (randint(1, max_y - 2), randint(1, max_x - 2))
        )
    return stars
