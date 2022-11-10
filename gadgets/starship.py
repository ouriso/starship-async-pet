from random import randrange
from types import coroutine

from gadgets.space_objects import SpaceObject
from gun import fire


class StarShip(SpaceObject):
    position_x: int = None
    position_y: int = None

    def fire(self, canvas) -> coroutine:
        fire_routine = fire(
            canvas, self.position_y, self.position_x + 2,
            randrange(-10, 0, 1) / 10,
            randrange(-10, 10, 1) / 10
        )
        return fire_routine
