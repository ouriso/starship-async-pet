from os import listdir, path
from random import choice, randint

from entities.space_objects import SpaceObject
from utils.canvas_dimensions import get_canvas_dimensions
from utils.frames import draw_frame, get_frame_size, get_frames_list
from utils.sleep import sleep


class Garbage(SpaceObject):
    async def animate(self, canvas) -> None:
        height, width = get_canvas_dimensions()

        while self.position_y < height:
            draw_frame(
                canvas, self.position_y, self.position_x, self.frames[0]
            )
            await sleep()
            draw_frame(
                canvas, self.position_y, self.position_x,
                self.frames[0], negative=True
            )
            self.position_y += self.offset_step_y


def generate_garbage() -> Garbage:
    frames_dir = './animations/garbage'
    height, width = get_canvas_dimensions()
    files_with_frames = listdir(frames_dir)
    frame_file = path.join(frames_dir, choice(files_with_frames))
    garbage_frames = get_frames_list([frame_file])
    frame_height, frame_width = get_frame_size(garbage_frames[0])

    pos_x = randint(3 - frame_width, width - 3)
    pos_y = 1 - frame_height

    return Garbage(pos_y, pos_x, garbage_frames, 1, 0)
