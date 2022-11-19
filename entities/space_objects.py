from abc import ABC
from itertools import cycle
from typing import Sequence

from entities.common import (
    ObjectBorders, ObjectAxesParams, ObjectSize,
    FrameStage
)
from utils.canvas_dimensions import get_canvas_dimensions
from utils.frames import draw_frame, get_frame_size
from utils.sleep import sleep


class SpaceObject(ABC):
    stages: FrameStage = ()

    def __init__(self, start_position_y: int, start_position_x: int,
                 frames: Sequence[str],
                 offset_step_y: int = 5, offset_step_x: int = 10):
        self.position_x = start_position_x
        self.position_y = start_position_y
        self.frames = frames
        self.offset_step_x = offset_step_x
        self.offset_step_y = offset_step_y

    @property
    def dimensions(self) -> ObjectSize:
        """
        Returns self dimensions by y and x axes.
        :return: self height and width
        """
        return get_frame_size(self.frames[0])

    @property
    def current_position(self) -> ObjectAxesParams:
        """
        Returns self current position by y and x axes.
        :return: y and x coordinates as the starting point for drawing the frame
        """
        return ObjectAxesParams(axis_y=self.position_y, axis_x=self.position_x)

    def object_borders(self) -> ObjectBorders:
        """
        Returns the coordinates of all self borders.
        :return: top, bottom, left and right coordinates
        """
        return ObjectBorders(
            top=self.position_y,
            bottom=self.position_y + self.dimensions.height,
            left=self.position_x,
            right=self.position_x + self.dimensions.width
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
        for object_frame in cycle(self.frames):
            await self.change_frame_stages(canvas, object_frame)

    async def change_frame_stages(self, canvas, object_frame):
        """
        Draws and removes current frame sequentially.
        :param canvas: current WindowObject
        :param object_frame: current frame to draw
        :return:
        """
        pos_y = self.position_y
        pos_x = self.position_x
        for lifetime, style in self.stages:
            draw_frame(
                canvas, pos_y, pos_x,
                object_frame, style
            )
            if lifetime:
                await sleep(lifetime)

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
        height, width = get_canvas_dimensions()
        min_y = min_x = 1
        offset_y = self.offset_step_y * offset_y
        offset_x = self.offset_step_x * offset_x
        object_borders = self.object_borders()

        if offset_y < 0:
            offset_y = max(offset_y, min_y - object_borders.top)
        elif offset_y > 0:
            offset_y = min(offset_y, height - object_borders.bottom - 1)
        if offset_x < 0:
            offset_x = max(offset_x, min_x - object_borders.left)
        elif offset_x > 0:
            offset_x = min(offset_x, width - object_borders.right - 1)

        return offset_y, offset_x
