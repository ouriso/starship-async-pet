from random import choice, randint
from typing import Optional

from entities.obstacle import Obstacle, get_obstacles
from entities.space_objects import SpaceObject
from utils.canvas_dimensions import get_canvas_dimensions
from utils.event_loop import append_coroutine
from utils.frames import get_frame_size, get_frames_from_file, update_frame
from utils.game_year import get_current_year
from utils.sleep import sleep


class Garbage(SpaceObject):

    async def animate(self, canvas) -> None:
        """
        Animates object moving.
        :param canvas: current WindowObject
        :return:
        """
        height, width = get_canvas_dimensions()

        while self.position_y < height:
            if self.need_to_stop:
                append_coroutine(self.explode(canvas))
                get_obstacles().remove(self)
                return
            await update_frame(
                canvas, self.position_y, self.position_x, self.frame, 3
            )

            self.position_y += self.speed_by_y


async def generate_garbage(canvas) -> None:
    """
    Generates various garbage in space depending on the current game year.
    :param canvas: current WindowObject
    """
    height, width = get_canvas_dimensions()
    obstacles = get_obstacles()

    garbage_frames = get_frames_from_file('./animations/garbage.txt')

    while True:
        creation_delay = get_garbage_delay_tics(get_current_year())
        if not creation_delay:
            # if delay is None - there is no garbage yet
            await sleep()
            continue
        await sleep(creation_delay)
        frame = choice(garbage_frames)
        frame_height, frame_width = get_frame_size(frame)

        pos_x = randint(3 - frame_width, width - 3)
        pos_y = 1 - frame_height
        new_garbage = Garbage(pos_y, pos_x, frame, 1, 0)

        # extending global variables with new objects
        append_coroutine(new_garbage.animate(canvas))
        obstacles.append(Obstacle(new_garbage))


def get_garbage_delay_tics(year) -> Optional[int]:
    """
    Calculates the delay between the creation of new garbage objects
    depending on the current game year.
    :param year: current game year
    :return: calculated delay
    """
    if year < 1961:
        return None
    elif year < 1969:
        return 20
    elif year < 1981:
        return 14
    elif year < 1995:
        return 10
    elif year < 2010:
        return 8
    elif year < 2020:
        return 6
    else:
        return 2
