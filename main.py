import curses
import time
from typing import List

from config import STARS_DENSITY, INIT_POS_RATIO_Y, INIT_POS_RATIO_X
from controls import read_controls
from entities.star import generate_stars
from gadgets.starship import BaseStarShip
from utils.canvas_dimensions import set_canvas_dimensions, get_canvas_dimensions


def main(canvas):
    curses.curs_set(False)
    set_canvas_dimensions(canvas)
    draw(canvas)


def draw(canvas):
    height, width = get_canvas_dimensions()
    stars_number = round(width * height / STARS_DENSITY)

    start_y = round(height * INIT_POS_RATIO_Y)
    start_x = round(width * INIT_POS_RATIO_X)

    stars = generate_stars(height, width, stars_number)
    starship = BaseStarShip(start_y, start_x, get_starship_frames())

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


def get_starship_frames() -> List[str]:
    with open(r'./animations/ship_frame_1.txt', 'r', encoding='utf-8') as fp:
        ship_frame_1 = fp.read()

    with open(r'./animations/ship_frame_2.txt', 'r', encoding='utf-8') as fp:
        ship_frame_2 = fp.read()
    ship_frames = [ship_frame_1, ship_frame_1, ship_frame_2, ship_frame_2]
    return ship_frames


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)

