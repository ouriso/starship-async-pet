import curses
from random import randint, choice
from typing import Set, Sequence

from entities.common import FrameStage
from entities.space_objects import SpaceObject
from utils.canvas_dimensions import get_canvas_dimensions
from utils.sleep import sleep, calculate_ticks_number


class Star(SpaceObject):
    """
    SpaceObject as a sparkling star.
    """
    stages: FrameStage = (
        FrameStage(calculate_ticks_number(0.3), curses.A_DIM),
        FrameStage(calculate_ticks_number(0.5), curses.A_NORMAL),
        FrameStage(calculate_ticks_number(1.0), curses.A_BOLD),
        FrameStage(calculate_ticks_number(0.3), curses.A_NORMAL)
    )

    def __init__(self, start_position_y: int, start_position_x: int,
                 frames: Sequence[str], appearance_delay: int):
        super().__init__(start_position_y, start_position_x, frames)
        self.appearance_delay = appearance_delay

    async def animate(self, canvas) -> None:
        await sleep(self.appearance_delay)
        for lifetime, style in self.stages:
            canvas.addstr(
                self.position_y, self.position_x,
                self.frames[0], style or curses.A_NORMAL)
            await sleep(lifetime)


def generate_stars(stars_number: int = 50) -> Set[Star]:
    """
    Randomly generates new set of stars.
    :param stars_number: number of stars to be generated
    :return: set of new Stars
    """
    height, width = get_canvas_dimensions()
    stars_symbols = ['*', ':', '.', '+']

    stars = set()
    for _ in range(stars_number):
        star = Star(
            randint(1, height), randint(1, width),
            [choice(stars_symbols)], calculate_ticks_number(randint(0, 3))
        )
        stars.add(star)
    return stars
