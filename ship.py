from frames import draw_frame
from utils.sleep import do_sleep

ship_stages = [False, True]


async def ship_animate(canvas, ship_y, ship_x, ship_frame):
    for is_negative in ship_stages:
        draw_frame(
            canvas, ship_y, ship_x,
            ship_frame, is_negative
        )
        await do_sleep()
