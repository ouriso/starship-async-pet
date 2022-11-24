from os import listdir, path
from random import choice, randint

from entities.space_objects import SpaceObject
from utils.canvas_dimensions import get_canvas_dimensions
from utils.event_loop import append_coroutine
from utils.frames import draw_frame, get_frame_size, get_frames_list
from utils.sleep import sleep


class Garbage(SpaceObject):
    async def animate(self, canvas) -> None:
        height, width = get_canvas_dimensions()

        while self.position_y < height:
            draw_frame(
                canvas, self.position_y, self.position_x, self.frames[0]
            )
            await sleep(3)
            draw_frame(
                canvas, self.position_y, self.position_x,
                self.frames[0], negative=True
            )
            self.position_y += self.offset_step_y


async def generate_garbage(canvas) -> None:
    height, width = get_canvas_dimensions()

    frames_dir = './animations/garbage'
    files_with_frames = [
        path.join(frames_dir, file_name) for file_name in listdir(frames_dir)]

    while True:
        await sleep(randint(4, 15))
        garbage_frames = get_frames_list([choice(files_with_frames)])
        frame_height, frame_width = get_frame_size(garbage_frames[0])

        pos_x = randint(3 - frame_width, width - 3)
        pos_y = 1 - frame_height

        new_garbage = Garbage(pos_y, pos_x, garbage_frames, 1, 0)
        append_coroutine(new_garbage.animate(canvas))
