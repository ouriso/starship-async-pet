import curses
import time
from random import randint

from config import STARS_NUMBER, BASE_DELAY
from controls import read_controls
from entities.star import generate_stars
from gadgets.starship import StarShip

with open(r'./animations/ship_frame_1.txt', 'r', encoding='utf-8') as fp:
    ship_frame_1 = fp.read()

with open(r'./animations/ship_frame_2.txt', 'r', encoding='utf-8') as fp:
    ship_frame_2 = fp.read()
ship_frames = [ship_frame_1, ship_frame_1, ship_frame_2, ship_frame_2]


def draw(canvas):
    curses.curs_set(False)
    max_y, max_x = curses.window.getmaxyx(canvas)

    start_y, start_x = (
        round(max_y * 3 / 4), round(max_x / 2)
    )

    stars = generate_stars(max_y, max_x, STARS_NUMBER)
    starship = StarShip(start_y, start_x, ship_frames)

    canvas.nodelay(True)

    active_coroutines = [
        [0, starship.animate(canvas)],
        *[[randint(0, 5), star.animate(canvas)] for star in stars]
    ]
    sleeping_coroutines = []

    while True:
        canvas.border()

        for _, coroutine in active_coroutines:
            try:
                sleep_command = coroutine.send(None)
                canvas.refresh()
            except StopIteration:
                continue
            seconds_to_sleep = sleep_command.seconds
            sleeping_coroutines.append([seconds_to_sleep, coroutine])

        sleeping_coroutines = [
            [timeout - BASE_DELAY, coroutine]
            for timeout, coroutine in sleeping_coroutines]

        # делим бомбы на активные и спящие
        active_coroutines = [
            [timeout, coroutine]
            for timeout, coroutine in sleeping_coroutines if timeout <= 0]
        sleeping_coroutines = [
            [timeout, coroutine]
            for timeout, coroutine in sleeping_coroutines if timeout > 0]

        y_offset, x_offset, need_fire = read_controls(canvas)
        starship.change_position(y_offset, x_offset)
        if need_fire:
            sleeping_coroutines.append([0, starship.fire(canvas)])

        time.sleep(BASE_DELAY)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
