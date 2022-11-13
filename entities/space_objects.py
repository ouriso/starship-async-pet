from abc import ABC
from typing import Sequence

from config import BASE_DELAY
from entities.common import (
    ObjectBorders, ObjectAxesParams, ObjectSize,
    FrameStage
)
from utils.canvas_params import get_border_params
from utils.frames import draw_frame, get_frame_size
from utils.sleep import Sleep


class SpaceObject(ABC):
    stages: FrameStage = ()

    def __init__(self, start_position_y: int, start_position_x: int,
                 frames: Sequence[str],
                 offset_step_y: int = 10, offset_step_x: int = 5):
        self.position_x = start_position_x
        self.position_y = start_position_y
        self.frames = frames
        self.offset_step_x = offset_step_x
        self.offset_step_y = offset_step_y

    @property
    def size(self) -> ObjectSize:
        return get_frame_size(self.frames[0])

    @property
    def current_position(self) -> ObjectAxesParams:
        return ObjectAxesParams(axis_y=self.position_y, axis_x=self.position_x)

    def object_borders(self) -> ObjectBorders:
        return ObjectBorders(
            top=self.position_y,
            bottom=self.position_y + self.size.height,
            left=self.position_x,
            right=self.position_x + self.size.width
        )

    def change_position(self, offset_y: int, offset_x: int) -> None:
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
        for object_frame in self.frames:
            await self.change_frame_stages(canvas, object_frame)

    async def change_frame_stages(self, canvas, object_frame):
        for lifetime, style in self.stages:
            draw_frame(
                canvas, self.position_y, self.position_x,
                object_frame, style
            )
            await Sleep(BASE_DELAY * lifetime)

    def offsets_calc(
            self, offset_y: int, offset_x: int
    ) -> ObjectAxesParams:
        """
        Calculate if expected offsets possible.
        If not returns new possible values.
        :param offset_y: expected y-axis offset
        :param offset_x: expected x-axis offset
        :return:
        """
        max_y, max_x = get_border_params()
        min_y = min_x = 1
        offset_y = self.offset_step_y * offset_y
        offset_x = self.offset_step_x * offset_x
        object_borders = self.object_borders()

        if offset_y < 0:
            offset_y = max(offset_y, min_y - object_borders.top)
        if offset_y > 0:
            offset_y = min(offset_y, max_y - object_borders.bottom)
        if offset_x < 0:
            offset_x = max(offset_x, min_x - object_borders.left)
        if offset_x > 0:
            offset_x = min(offset_x, max_x - object_borders.right)

        return offset_y, offset_x
