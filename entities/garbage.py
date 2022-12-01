from random import choice, randint

from entities.obstacle import Obstacle, get_obstacles
from entities.space_objects import SpaceObject
from utils.canvas_dimensions import get_canvas_dimensions
from utils.event_loop import append_coroutine, get_coroutines
from utils.frames import get_frame_size, get_frames_from_file, \
    update_frame
from utils.sleep import sleep


class Garbage(SpaceObject):

    async def animate(self, canvas) -> None:
        height, width = get_canvas_dimensions()

        while self.position_y < height:
            if self.need_to_stop:
                coroutines = get_coroutines()
                coroutines.append(self.explode(canvas))
                get_obstacles().remove(self)
                return
            await update_frame(
                canvas, self.position_y, self.position_x, self.frame, 3
            )

            self.position_y += self.speed_by_y

    async def explode(self, canvas) -> None:
        explode_size = get_frame_size(self.explode_frames[0])
        center_y = self.position_y + self.dimensions.height / 2
        center_x = self.position_x + self.dimensions.width / 2
        explode_y = center_y - explode_size.height / 2
        explode_x = center_x - explode_size.width / 2
        for frame in self.explode_frames:
            await update_frame(canvas, explode_y, explode_x, frame)


async def generate_garbage(canvas) -> None:
    height, width = get_canvas_dimensions()
    obstacles = get_obstacles()

    garbage_frames = get_frames_from_file('./animations/garbage.txt')

    while True:
        await sleep(randint(4, 15))
        frame = choice(garbage_frames)
        frame_height, frame_width = get_frame_size(frame)

        pos_x = randint(3 - frame_width, width - 3)
        pos_y = 1 - frame_height

        new_garbage = Garbage(pos_y, pos_x, frame, 1, 0)
        append_coroutine(new_garbage.animate(canvas))
        obstacles.append(Obstacle(new_garbage))
