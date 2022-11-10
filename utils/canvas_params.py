import curses
from typing import Tuple

_CANVAS_WIDTH = 0
_CANVAS_HEIGHT = 0


def set_border_params(canvas) -> None:
    global _CANVAS_HEIGHT
    global _CANVAS_WIDTH

    if _CANVAS_WIDTH is None or _CANVAS_HEIGHT is None:
        max_y, max_x = curses.window.getmaxyx(canvas)
        _CANVAS_HEIGHT = max_y
        _CANVAS_WIDTH = max_x


def get_border_params() -> Tuple[int, int]:
    global _CANVAS_HEIGHT
    global _CANVAS_WIDTH

    return _CANVAS_HEIGHT, _CANVAS_WIDTH
