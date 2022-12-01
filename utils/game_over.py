from itertools import cycle

from entities.common import ObjectAxesParams
from entities.obstacle import check_object_collisions
from utils.canvas_dimensions import get_canvas_dimensions
from utils.frames import get_frames_from_file, get_frame_size, update_frame

positions_delta = (
    ObjectAxesParams(2, 2),
    ObjectAxesParams(-2, 2),
    ObjectAxesParams(2, -2),
    ObjectAxesParams(-2, -2),
)


async def game_over_animate(canvas):
    frame: str = get_frames_from_file(r'./animations/game_over.txt')[0]
    frame_size = get_frame_size(frame)
    height, width = get_canvas_dimensions()
    start_pos_y = height / 2 - frame_size.height / 2
    start_pos_x = width / 2 - frame_size.width / 2

    for offset_y, offset_x in cycle(positions_delta):
        check_object_collisions(
            start_pos_y, start_pos_x, frame_size.height, frame_size.width
        )
        await update_frame(canvas, start_pos_y, start_pos_x, frame, 10)
        start_pos_y += offset_y
        start_pos_x += offset_x
