from os import listdir, path
from random import choice, randint

from entities.obstacle import Obstacle, get_obstacles
from entities.space_objects import SpaceObject
from utils.canvas_dimensions import get_canvas_dimensions
from utils.event_loop import append_coroutine, get_coroutines
from utils.frames import draw_frame, get_frame_size, get_frames_from_files
from utils.sleep import sleep


class Garbage(SpaceObject):
    explode_frames = get_frames_from_files(
        r'./animations/explosion.txt'
    ).split(',\n')

    async def animate(self, canvas) -> None:
        height, width = get_canvas_dimensions()

        while self.position_y < height:
            if self.need_to_stop:
                coroutines = get_coroutines()
                coroutines.append(self.explode(canvas))
                get_obstacles().remove(self)
                return
            draw_frame(
                canvas, self.position_y, self.position_x, self.frame
            )
            await sleep(3)
            draw_frame(
                canvas, self.position_y, self.position_x,
                self.frame, negative=True
            )
            self.position_y += self.speed_by_y

    async def explode(self, canvas) -> None:
        explode_size = get_frame_size(self.explode_frames[0])
        center_y = self.position_y + (
                self.object_borders().bottom - self.object_borders().top) / 2
        center_x = self.position_x + (
                self.object_borders().right - self.object_borders().left) / 2
        explode_y = center_y - explode_size.height / 2
        explode_x = center_x - explode_size.width / 2
        for frame in self.explode_frames:
            draw_frame(
                canvas, explode_y, explode_x, frame
            )
            await sleep(2)
            draw_frame(
                canvas, explode_y, explode_x, frame, negative=True
            )


async def generate_garbage(canvas) -> None:
    height, width = get_canvas_dimensions()
    obstacles = get_obstacles()

    frames_dir = './animations/garbage'
    files_with_frames = [
        path.join(frames_dir, file_name) for file_name in listdir(frames_dir)]

    while True:
        await sleep(randint(4, 15))
        garbage_frames = get_frames_from_files(choice(files_with_frames))
        frame_height, frame_width = get_frame_size(garbage_frames)

        pos_x = randint(3 - frame_width, width - 3)
        pos_y = 1 - frame_height

        new_garbage = Garbage(pos_y, pos_x, garbage_frames, 1, 0)
        append_coroutine(new_garbage.animate(canvas))
        obstacles.append(Obstacle(new_garbage))
