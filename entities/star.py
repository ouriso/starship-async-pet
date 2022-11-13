import curses
from random import randint, choice
from typing import Set

from config import BASE_DELAY
from entities.common import FrameStage
from entities.space_objects import SpaceObject
from utils.sleep import Sleep

stars_symbols = ['*', ':', '.', '+']


class Star(SpaceObject):
    stars_stages = (
        FrameStage(BASE_DELAY, curses.A_DIM),
        FrameStage(3 * BASE_DELAY, curses.A_NORMAL),
        FrameStage(5 * BASE_DELAY, curses.A_BOLD),
        FrameStage(2 * BASE_DELAY, curses.A_NORMAL)
    )

    async def change_frame_stages(self, canvas, object_frame):
        while True:
            for lifetime, style in self.stages:
                canvas.addstr(
                    self.position_y, self.position_x,
                    object_frame, style or curses.A_NORMAL)
                await Sleep(BASE_DELAY * lifetime)


def generate_stars(
        max_y: int, max_x: int, stars_number: int = 50
) -> Set[Star]:
    stars = set()
    for _ in range(stars_number):
        star = Star(
            randint(1, max_y - 2), randint(1, max_x - 2),
            [choice(stars_symbols)], 0, 0
        )
        stars.add(star)
    return stars
