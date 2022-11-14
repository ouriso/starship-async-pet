from types import coroutine
from typing import Sequence

from config import BASE_DELAY
from entities.common import FrameStage
from entities.space_objects import SpaceObject
from gadgets.guns import OldTroopersBlaster


class StarShip(SpaceObject):
    stages = (
        FrameStage(BASE_DELAY, False),
        FrameStage(0, True)
    )

    def __init__(self, start_position_y: int, start_position_x: int,
                 frames: Sequence[str]):
        super().__init__(start_position_y, start_position_x, frames)
        self.gun = OldTroopersBlaster()

    def fire(self, canvas) -> coroutine:
        fire_routine = self.gun.fire(
            canvas, self.position_y, self.position_x + 2
        )
        return fire_routine
