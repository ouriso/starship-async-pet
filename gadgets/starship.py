from itertools import cycle
from types import coroutine
from typing import Sequence

from entities.space_objects import SpaceObject
from gadgets.guns import OldTroopersBlaster
from utils.frames import draw_frame
from utils.sleep import sleep


class BaseStarShip(SpaceObject):
    """
    Implements the positioning of a starship in the current window.
    """
    frame_lifetime = 4

    def __init__(self, start_position_y: int, start_position_x: int,
                 frames: Sequence[str]):
        super().__init__(start_position_y, start_position_x, frames)
        self.gun = OldTroopersBlaster()

    def fire(self, canvas) -> coroutine:
        """
        Creates coroutine with shot animation.
        :param canvas: current WindowObject
        :return: animation of firing
        """
        # the shooting animation starts at the top of the ship
        # and in the middle of its width
        fire_routine = self.gun.fire(
            canvas, self.position_y,
            self.position_x + round(self.dimensions.width / 2)
        )
        return fire_routine

    async def animate(self, canvas) -> None:
        """
        Animates ship moving.
        :param canvas: current WindowObject
        :return:
        """
        for frame in cycle(self.frames):
            # saving the current position to prevent incorrect erasing
            pos_y = self.position_y
            pos_x = self.position_x
            draw_frame(canvas, pos_y, pos_x, frame)
            await sleep(self.frame_lifetime)
            draw_frame(canvas, pos_y, pos_x, frame, True)
