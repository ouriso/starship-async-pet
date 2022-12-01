import curses
import time

from config import STARS_DENSITY, INIT_POS_RATIO_Y, INIT_POS_RATIO_X, BASE_DELAY
from entities.garbage import generate_garbage
from entities.star import generate_stars
from gadgets.starship import BaseStarShip
from utils.canvas_dimensions import set_canvas_dimensions, get_canvas_dimensions
from utils.event_loop import get_coroutines
from utils.frames import get_frames_from_file
from utils.game_year import animate_year


def main(canvas):
    curses.curs_set(False)
    set_canvas_dimensions(canvas)
    canvas.nodelay(True)
    draw(canvas)


def draw(canvas):
    """Main drawings."""
    height, width = get_canvas_dimensions()
    stars_number = round(width * height / STARS_DENSITY)

    start_y = round(height * INIT_POS_RATIO_Y)
    start_x = round(width * INIT_POS_RATIO_X)

    stars = generate_stars(stars_number)
    starship_frames = get_frames_from_file('./animations/ship_frame.txt')
    starship = BaseStarShip(
        start_y, start_x, starship_frames
    )
    new_win = canvas.derwin(6, 40, height - 6, width - 40)

    coroutines = get_coroutines()
    coroutines.extend([
        *[star.animate(canvas) for star in stars],
        starship.run_starship(canvas),
        generate_garbage(canvas),
        animate_year(new_win)
    ])

    while True:
        canvas.border()
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.refresh()
        time.sleep(BASE_DELAY)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
