import curses
from itertools import cycle
from random import randint, choice
from typing import Set, Sequence

from entities.common import FrameStage
from entities.space_objects import SpaceObject
from utils.canvas_dimensions import get_canvas_dimensions
from utils.sleep import sleep, calculate_ticks_number


class Star(SpaceObject):
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
        for object_frame in cycle(self.frames):
            await self.change_frame_stages(canvas, object_frame)

    async def change_frame_stages(self, canvas, object_frame):
        for lifetime, style in self.stages:
            canvas.addstr(
                self.position_y, self.position_x,
                object_frame, style or curses.A_NORMAL)
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
            randint(1, height - 1), randint(1, width - 1),
            [choice(stars_symbols)], calculate_ticks_number(randint(0, 3))
        )
        stars.add(star)
    return stars
