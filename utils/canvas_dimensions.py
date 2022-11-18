import curses

from entities.common import ObjectSize

_CANVAS_WIDTH = None
_CANVAS_HEIGHT = None


def set_canvas_dimensions(canvas) -> None:
    global _CANVAS_HEIGHT
    global _CANVAS_WIDTH

    if _CANVAS_WIDTH is None or _CANVAS_HEIGHT is None:
        max_y, max_x = curses.window.getmaxyx(canvas)
        _CANVAS_HEIGHT = max_y - 1
        _CANVAS_WIDTH = max_x - 1


def get_canvas_dimensions() -> ObjectSize:
    global _CANVAS_HEIGHT
    global _CANVAS_WIDTH

    return ObjectSize(height=_CANVAS_HEIGHT, width=_CANVAS_WIDTH)
