from abc import ABC, abstractmethod
from typing import Sequence, Union

from entities.common import (
    ObjectBorders, ObjectSize,
    FrameStage
)
from utils.canvas_dimensions import get_canvas_dimensions
from utils.frames import get_frame_size


class SpaceObject(ABC):
    """
    Abstract class that implements the positioning of an object
     in the current window.
    """
    stages: FrameStage = ()

    def __init__(self, start_position_y: int, start_position_x: int,
                 frames: Union[str, Sequence[str]],
                 speed_by_y: int = 5, speed_by_x: int = 10):
        self.position_x = start_position_x
        self.position_y = start_position_y
        self.frames = frames
        self.speed_by_y = speed_by_y
        self.speed_by_x = speed_by_x

    @property
    def frame(self) -> str:
        if isinstance(self.frames, str):
            return self.frames
        else:
            return self.frames[0]

    @property
    def dimensions(self) -> ObjectSize:
        """
        Returns self dimensions by y and x axes.
        :return: self height and width
        """
        return get_frame_size(self.frame)

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

    @abstractmethod
    async def animate(self, canvas) -> None:
        """
        Animates object moving.
        :param canvas: current WindowObject
        :return:
        """

    def change_position(self, offset_y: int, offset_x: int) -> None:
        """
        Changes the position of the object depending on the offset arguments
        and maximum available offset values.
        :param offset_y: y-axis offset direction
        :param offset_x: x-axis offset direction
        :return:
        """
        height, width = get_canvas_dimensions()
        min_y = min_x = 1
        # calculate expected offset values
        offset_y = self.speed_by_y * offset_y
        offset_x = self.speed_by_x * offset_x
        object_borders = self.object_borders()

        if offset_y < 0:
            offset_y = max(offset_y, min_y - object_borders.top)
        elif offset_y > 0:
            offset_y = min(offset_y, height - object_borders.bottom)
        if offset_x < 0:
            offset_x = max(offset_x, min_x - object_borders.left)
        elif offset_x > 0:
            offset_x = min(offset_x, width - object_borders.right)

        self.position_y += offset_y
        self.position_x += offset_x
