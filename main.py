import time
import curses
from random import randint, randrange

from controls import read_controls
from gun import fire
from ship import ship_animate
from stars import blink, generate_stars

with open(r'./animations/ship_frame_1.txt', 'r', encoding='utf-8') as fp:
    ship_frame_1 = fp.read()

with open(r'./animations/ship_frame_2.txt', 'r', encoding='utf-8') as fp:
    ship_frame_2 = fp.read()
ship_frames = [ship_frame_1, ship_frame_2]


def draw(canvas):
    curses.curs_set(False)
    max_y, max_x = curses.window.getmaxyx(canvas)

    start_y, start_x = (
        max_y * 3 / 4, max_x / 2
    )

    stars = generate_stars(max_y, max_x)

    canvas.border()
    canvas.refresh()

    corutines_add = [
        blink(canvas, row, column, randint(10, 70)) for row, column in stars
    ]
    corutines = [
        *corutines_add,
        ship_animate(canvas, start_y, start_x)
    ]
    sleeping_corutines = [[0, corutine] for corutine in corutines]

    while True:
        min_delay, _ = min(sleeping_corutines, key=lambda pair: pair[0])
        sleeping_corutines = [
            [timeout - min_delay, bomb] for timeout, bomb in sleeping_corutines]
        time.sleep(min_delay)

        # делим бомбы на активные и спящие
        active_corutines = [
            [timeout, bomb] for timeout, bomb in sleeping_corutines if timeout <= 0
        ]
        sleeping_corutines = [
            [timeout, bomb] for timeout, bomb in sleeping_corutines if timeout > 0]

        for _, corutine in active_corutines:
            try:
                sleep_command = corutine.send(None)
                canvas.refresh()
                seconds_to_sleep = sleep_command.seconds
                time.sleep(seconds_to_sleep)
                sleeping_corutines.append([seconds_to_sleep, corutine])
            except StopIteration:
                continue

        y_offset, x_offset, need_fire = read_controls(canvas)
        start_y += y_offset
        start_x += x_offset
        if need_fire:
            sleeping_corutines.append(
                [0, fire(
                    canvas, start_y - 1, start_x + 2,
                    randrange(-10, 10, 1) / 10,
                    randrange(-10, 10, 1) / 10
                )]
            )

        time.sleep(0.2)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
