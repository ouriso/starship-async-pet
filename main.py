import curses
import time

from config import STARS_NUMBER
from controls import read_controls
from entities.star import generate_stars
from gadgets.starship import BaseStarShip
from utils.canvas_params import set_border_params, get_border_params

with open(r'./animations/ship_frame_1.txt', 'r', encoding='utf-8') as fp:
    ship_frame_1 = fp.read()

with open(r'./animations/ship_frame_2.txt', 'r', encoding='utf-8') as fp:
    ship_frame_2 = fp.read()
ship_frames = [ship_frame_1, ship_frame_1, ship_frame_2, ship_frame_2]


def draw(canvas):
    curses.curs_set(False)
    set_border_params(canvas)
    max_y, max_x = get_border_params()

    start_y, start_x = (
        round(max_y * 3 / 4), round(max_x / 2)
    )

    stars = generate_stars(max_y, max_x, STARS_NUMBER)
    starship = BaseStarShip(start_y, start_x, ship_frames)

    canvas.nodelay(True)

    sleeping_coroutines = [
        *[[0, star.animate(canvas)] for star in stars],
        [0, starship.animate(canvas)]
    ]

    while True:
        canvas.border()

        min_sleep, _ = min(sleeping_coroutines, key=lambda pair: pair[0])
        sleeping_coroutines = [
            [timeout - min_sleep, coroutine]
            for timeout, coroutine in sleeping_coroutines]

        # делим корутины на активные и спящие
        active_coroutines = [
            [timeout, coroutine]
            for timeout, coroutine in sleeping_coroutines if timeout <= 0]
        sleeping_coroutines = [
            [timeout, coroutine]
            for timeout, coroutine in sleeping_coroutines if timeout > 0]

        for _, coroutine in active_coroutines:
            try:
                sleep_command = coroutine.send(None)
                canvas.refresh()
            except StopIteration:
                continue
            seconds_to_sleep = sleep_command.seconds
            sleeping_coroutines.append([seconds_to_sleep, coroutine])

        y_offset, x_offset, need_fire = read_controls(canvas)
        if y_offset != 0 or x_offset != 0:
            starship.change_position(y_offset, x_offset)
        if need_fire:
            sleeping_coroutines.append([0, starship.fire(canvas)])

        time.sleep(min_sleep)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
