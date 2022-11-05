import curses

from frames import draw_frame, get_frame_size
from utils.sleep import do_sleep

ship_stages = [False, True]


async def ship_animate(canvas, ship_y, ship_x, ship_frame):
    for is_negative in ship_stages:
        draw_frame(
            canvas, ship_y, ship_x,
            ship_frame, is_negative
        )
        await do_sleep()


def offsets_calc(canvas, text, current_y, current_x, offset_y, offset_x):
    max_y, max_x = curses.window.getmaxyx(canvas)
    min_y = min_x = 1
    
    rows, columns = get_frame_size(text)

    x_left, x_right = current_x + offset_x, current_x + offset_x + columns
    y_upper, y_lower = current_y + offset_y, current_y + offset_y + rows

    if x_left >= min_x and x_right <= max_x:
        offset_x = offset_x
    else:
        if offset_x < 0:
            offset_x = offset_x - x_left
        elif offset_x > 0:
            offset_x = offset_x - (x_right - max_x)

    if y_upper >= min_y and y_lower <= max_y:
        offset_y = offset_y
    else:
        if offset_y < 0:
            offset_y = offset_y - y_upper
        elif offset_y > 0:
            offset_y = offset_y - (y_lower - max_y)

    return offset_y, offset_x
