import curses
import time

from config import STARS_DENSITY, INIT_POS_RATIO_Y, INIT_POS_RATIO_X, BASE_DELAY
from controls import read_controls
from entities.star import generate_stars
from gadgets.starship import BaseStarShip
from utils.canvas_dimensions import set_canvas_dimensions, get_canvas_dimensions
from utils.frames import get_frames_list


def main(canvas):
    curses.curs_set(False)
    set_canvas_dimensions(canvas)
    canvas.nodelay(True)
    draw(canvas)


def draw(canvas):
    """Main drawings."""
    max_y, max_x = get_canvas_dimensions()
    stars_number = round(max_x * max_y / STARS_DENSITY)

    start_y = round(max_y * INIT_POS_RATIO_Y)
    start_x = round(max_x * INIT_POS_RATIO_X)

    stars = generate_stars(stars_number)
    starship_frames = ['./animations/ship_frame_1.txt',
                       './animations/ship_frame_2.txt']
    starship = BaseStarShip(
        start_y, start_x, get_frames_list(starship_frames)
    )

    coroutines = [
        *[star.animate(canvas) for star in stars],
        starship.animate(canvas)
    ]

    while True:
        canvas.border()

        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        y_offset, x_offset, need_fire = read_controls(canvas)
        if y_offset != 0 or x_offset != 0:
            starship.change_position(y_offset, x_offset)
        if need_fire:
            coroutines.append(starship.fire(canvas))

        canvas.refresh()
        time.sleep(BASE_DELAY)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
