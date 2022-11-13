import curses
from itertools import cycle
from random import randint, choice
from typing import Set, Sequence

from entities.common import FrameStage
from entities.space_objects import SpaceObject
from utils.sleep import Sleep

stars_symbols = ['*', ':', '.', '+']


class Star(SpaceObject):
    stages: FrameStage = (
        FrameStage(0.3, curses.A_DIM),
        FrameStage(0.5, curses.A_NORMAL),
        FrameStage(1.0, curses.A_BOLD),
        FrameStage(0.3, curses.A_NORMAL)
    )

    def __init__(self, start_position_y: int, start_position_x: int,
                 frames: Sequence[str], appearance_delay: int):
        super().__init__(start_position_y, start_position_x, frames)
        self.appearance_delay = appearance_delay

    async def animate(self, canvas) -> None:
        await Sleep(self.appearance_delay)
        for object_frame in cycle(self.frames):
            await self.change_frame_stages(canvas, object_frame)

    async def change_frame_stages(self, canvas, object_frame):
        for lifetime, style in self.stages:
            canvas.addstr(
                self.position_y, self.position_x,
                object_frame, style or curses.A_NORMAL)
            await Sleep(lifetime)


def generate_stars(
        max_y: int, max_x: int, stars_number: int = 50
) -> Set[Star]:
    stars = set()
    for _ in range(stars_number):
        star = Star(
            randint(1, max_y - 2), randint(1, max_x - 2),
            [choice(stars_symbols)], randint(0, 5)
        )
        stars.add(star)
    return stars
