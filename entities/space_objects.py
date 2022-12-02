from abc import ABC, abstractmethod
from typing import Sequence, Union

from entities.common import (
    ObjectBorders, ObjectSize,
    FrameStage
)
from utils.frames import get_frame_size, get_frames_from_file, update_frame


class SpaceObject(ABC):
    """
    Abstract class that implements the positioning of an object
     in the current window.
    """
    explode_frames = get_frames_from_file(r'./animations/explosion.txt')
    stages: FrameStage = ()
    need_to_stop: bool = False

    def __init__(self, start_position_y: int, start_position_x: int,
                 frames: Union[str, Sequence[str]],
                 speed_by_y: int = 0, speed_by_x: int = 0):
        self.position_x = start_position_x
        self.position_y = start_position_y
        self.frames = frames
        self.speed_by_y = speed_by_y
        self.speed_by_x = speed_by_x

    @property
    def frame(self) -> str:
        """
        Returns the first frame of the object.
        :return: first frame
        """
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

    def set_need_to_stop(self):
        """
        Sets a flag indicating that the animation coroutine should stop.
        """
        self.need_to_stop = True

    async def explode(self, canvas) -> None:
        """
        Explosion animation after collision.
        :param canvas: current WindowObject
        """
        explode_size = get_frame_size(self.explode_frames[0])
        # calculate base position of the explosion size
        center_y = self.position_y + self.dimensions.height / 2
        center_x = self.position_x + self.dimensions.width / 2
        explode_y = center_y - explode_size.height / 2
        explode_x = center_x - explode_size.width / 2
        for frame in self.explode_frames:
            await update_frame(canvas, explode_y, explode_x, frame)
