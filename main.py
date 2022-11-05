import time
import curses
from itertools import cycle
from random import randint, randrange

from controls import read_controls
from gun import fire
from ship import ship_animate, offsets_calc
from stars import blink, generate_stars

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
    need_fire = False

    stars = generate_stars(max_y, max_x)

    canvas.nodelay(True)

    corutines_add = [
        blink(canvas, row, column, randint(10, 30)) for row, column in stars
    ]

    corutines = []

    for ship_frame in cycle(ship_frames):
        canvas.border()
        corutines.extend(corutines_add)
        corutines.append(ship_animate(canvas, start_y, start_x, ship_frame))
        if need_fire:
            corutines.append(
                fire(
                    canvas, start_y - 1, start_x + 2,
                    randrange(-10, 0, 1) / 10,
                    randrange(-10, 10, 1) / 10
                )
            )
        for corutine in corutines.copy():
            try:
                corutine.send(None)
                canvas.refresh()
            except StopIteration:
                corutines.remove(corutine)
                continue

        y_offset, x_offset, need_fire = read_controls(canvas)
        y_offset, x_offset = offsets_calc(canvas, ship_frame, start_y, start_x, y_offset, x_offset)
        start_y += y_offset
        start_x += x_offset

        time.sleep(0.1)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
