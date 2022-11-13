from random import randrange
from types import coroutine

from config import BASE_DELAY
from entities.common import FrameStage
from entities.space_objects import SpaceObject
from gun import fire


class StarShip(SpaceObject):
    stages = (
        FrameStage(BASE_DELAY, False),
        FrameStage(0, True)
    )

    def fire(self, canvas) -> coroutine:
        fire_routine = fire(
            canvas, self.position_y, self.position_x + 2,
            randrange(-10, 0, 1) / 10,
            randrange(-10, 10, 1) / 10
        )
        return fire_routine
