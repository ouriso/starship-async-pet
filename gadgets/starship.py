from types import coroutine
from typing import Sequence

from config import BASE_DELAY
from entities.common import FrameStage
from entities.space_objects import SpaceObject
from gadgets.guns import OldTroopersBlaster
from utils.sleep import calculate_ticks_number


class BaseStarShip(SpaceObject):
    stages = (
        FrameStage(calculate_ticks_number(2 * BASE_DELAY), False),
        FrameStage(0, True)
    )

    def __init__(self, start_position_y: int, start_position_x: int,
                 frames: Sequence[str]):
        super().__init__(start_position_y, start_position_x, frames)
        self.gun = OldTroopersBlaster()

    def fire(self, canvas) -> coroutine:
        # the shooting animation starts at the top of the ship
        # and in the middle of its width
        fire_routine = self.gun.fire(
            canvas, self.position_y,
            self.position_x + round(self.dimensions.width / 2)
        )
        return fire_routine
