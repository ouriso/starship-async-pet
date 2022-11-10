from abc import ABC
from itertools import cycle
from typing import Tuple, List

from config import BASE_DELAY
from utils.canvas_params import get_border_params
from utils.frames import draw_frame, get_frame_size
from utils.sleep import Sleep


class SpaceObject(ABC):

    def __init__(self, start_position_x: int, start_position_y: int,
                 frames: List[str],
                 offset_step_x: int = 10, offset_step_y: int = 5):
        self.position_x = start_position_x
        self.position_y = start_position_y
        self.frames = frames
        self.offset_step_x = offset_step_x
        self.offset_step_y = offset_step_y

    @property
    def size(self) -> Tuple[int, int]:
        return get_frame_size(self.frames[0])

    @property
    def current_position(self) -> Tuple[int, int]:
        return self.position_y, self.position_x

    async def change_position(self, offset_y: int, offset_x: int) -> None:
        """
        Offsets the object's position by the passed values.
        :param offset_y: y-axis offset
        :param offset_x: x-axis offset
        :return: None
        """
        offset_y, offset_x = self.offsets_calc(offset_y, offset_x)
        self.position_y += offset_y
        self.position_x += offset_x

    async def animate(self, canvas) -> None:
        """
        Animates object moving.
        :param canvas: current WindowObject
        :return:
        """
        for object_frame in cycle(self.frames):

            for is_negative in (False, True):
                draw_frame(
                    canvas, self.position_y, self.position_x,
                    object_frame, is_negative
                )
                await Sleep(BASE_DELAY)

    def offsets_calc(self, offset_y: int, offset_x: int) -> Tuple[int, int]:
        """
        Calculate if expected offsets possible.
        If not returns new possible values.
        :param offset_y: expected y-axis offset
        :param offset_x: expected x-axis offset
        :return:
        """
        # TODO: создать методы, определяющие по текущему положению
        #  максимально возможное смещение для корабля в каждую сторону
        max_y, max_x = get_border_params()
        min_y = min_x = 1

        rows, columns = self.size

        x_left = self.position_x + offset_x
        x_right = self.position_x + offset_x + columns
        y_upper = self.position_y + offset_y
        y_lower = self.position_y + offset_y + rows

        if x_left >= min_x and x_right <= max_x:
            offset_x = offset_x
        else:
            if offset_x < 0:
                offset_x = offset_x - x_left
            elif offset_x > 0:
                offset_x = offset_x - (x_right - max_x)

        if y_upper >= min_y and y_lower <= max_y:
            offset_y = offset_y
        else:
            if offset_y < 0:
                offset_y = offset_y - y_upper
            elif offset_y > 0:
                offset_y = offset_y - (y_lower - max_y)

        return offset_y, offset_x
