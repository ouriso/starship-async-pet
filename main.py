import curses
import time
from itertools import cycle
from random import randint, randrange

from config import STARS_NUMBER, BASE_DELAY
from controls import read_controls
from gun import fire
from ship import ship_animate, offsets_calc
from stars import generate_stars, star

with open(r'./animations/ship_frame_1.txt', 'r', encoding='utf-8') as fp:
    ship_frame_1 = fp.read()

with open(r'./animations/ship_frame_2.txt', 'r', encoding='utf-8') as fp:
    ship_frame_2 = fp.read()
ship_frames = [ship_frame_1, ship_frame_1, ship_frame_2, ship_frame_2]


def draw(canvas):
    curses.curs_set(False)
    max_y, max_x = curses.window.getmaxyx(canvas)

    start_y, start_x = (
        max_y * 3 / 4, max_x / 2
    )

    stars = generate_stars(max_y, max_x, STARS_NUMBER)

    canvas.nodelay(True)

    coroutines_stars = [
        [0, star(canvas, row, column, randint(1, 3), symbol)]
        for row, column, symbol in stars
    ]

    frames = cycle(ship_frames)
    need_fire = False

    while True:
        sleeping_coroutines = [
            *coroutines_stars
        ]

        while sleeping_coroutines:
            canvas.border()
            ship_frame = next(frames)

            sleeping_coroutines = [
                [timeout - BASE_DELAY, coroutine] for timeout, coroutine in sleeping_coroutines]
            time.sleep(BASE_DELAY)

            # делим бомбы на активные и спящие
            active_coroutines = [
                [timeout, coroutine] for timeout, coroutine in sleeping_coroutines if timeout <= 0]
            sleeping_coroutines = [
                [timeout, coroutine] for timeout, coroutine in sleeping_coroutines if timeout > 0]

            active_coroutines.append(
                [0, ship_animate(canvas, start_y, start_x, ship_frame)]
            )
            if need_fire:
                active_coroutines.append(
                    [0, fire(
                        canvas, start_y, start_x + 2,
                        randrange(-10, 0, 1) / 10,
                        randrange(-10, 10, 1) / 10
                    )]
                )

            for _, coroutine in active_coroutines:
                try:
                    sleep_command = coroutine.send(None)
                    canvas.refresh()
                except StopIteration:
                    continue
                seconds_to_sleep = sleep_command.seconds
                sleeping_coroutines.append([seconds_to_sleep, coroutine])

            y_offset, x_offset, need_fire = read_controls(canvas)
            y_offset, x_offset = offsets_calc(
                canvas, ship_frame, start_y, start_x, y_offset, x_offset
            )
            start_y += y_offset
            start_x += x_offset

            time.sleep(BASE_DELAY)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
