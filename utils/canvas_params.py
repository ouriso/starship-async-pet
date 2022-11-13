import curses

from entities.common import ObjectSize

_CANVAS_WIDTH = 0
_CANVAS_HEIGHT = 0


def set_border_params(canvas) -> None:
    global _CANVAS_HEIGHT
    global _CANVAS_WIDTH

    if _CANVAS_WIDTH is None or _CANVAS_HEIGHT is None:
        max_y, max_x = curses.window.getmaxyx(canvas)
        _CANVAS_HEIGHT = max_y
        _CANVAS_WIDTH = max_x


def get_border_params() -> ObjectSize:
    global _CANVAS_HEIGHT
    global _CANVAS_WIDTH

    return ObjectSize(height=_CANVAS_HEIGHT, width=_CANVAS_WIDTH)
