import asyncio
import time
from itertools import cycle

from frames import draw_frame, get_frame_size  # , read_controls
from utils.sleep import do_sleep

with open(r'./animations/ship_frame_1.txt', 'r', encoding='utf-8') as fp:
    ship_frame_1 = fp.read()
    rows_1, columns_1 = get_frame_size(ship_frame_1)
    square_1 = rows_1 * columns_1

with open(r'./animations/ship_frame_2.txt', 'r', encoding='utf-8') as fp:
    ship_frame_2 = fp.read()
    rows_2, columns_2 = get_frame_size(ship_frame_2)
    square_2 = rows_2 * columns_2

with open(r'./animations/ship.txt', 'r', encoding='utf-8') as fp:
    ship = fp.read()
    ship_rows, ship_columns = get_frame_size(ship_frame_2)

ship_frames = [
    ship_frame_1,
    ship_frame_2
]
ship_stages = [False, True]


async def ship_animate(canvas, ship_y, ship_x):
    for ship_frame in ship_frames:
        # draw_frame(canvas, ship_y, ship_x, ship)
        for is_negative in ship_stages:
            draw_frame(
                canvas, ship_y, ship_x,
                ship_frame, is_negative
            )
            # canvas.refresh()
            await do_sleep()
            # if not is_negative:
            #     time.sleep(0.1)
        # await asyncio.sleep(0)
        # draw_frame(canvas, ship_y, ship_x, ship, True)
        # canvas.refresh()
