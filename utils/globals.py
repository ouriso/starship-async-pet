import curses
from types import coroutine
from typing import List

from entities.common import ObjectSize

COROUTINES: List[coroutine] = []
OBSTACLES: list = []

_CANVAS_WIDTH = None
_CANVAS_HEIGHT = None


def set_canvas_dimensions(canvas) -> None:
    """
    Saves current window height and width.
    :param canvas: current WindowObject
    :return:
    """
    global _CANVAS_HEIGHT
    global _CANVAS_WIDTH

    if _CANVAS_WIDTH is None or _CANVAS_HEIGHT is None:
        # according to the documentation the function `getmaxyx()`
        # returns the height and width of the window
        height, width = curses.window.getmaxyx(canvas)
        # extreme positions of drawn objects
        _CANVAS_HEIGHT = height - 1
        _CANVAS_WIDTH = width - 1


def get_canvas_dimensions() -> ObjectSize:
    """
    Receives current window height and width.
    :return: window height and width
    """
    return ObjectSize(height=_CANVAS_HEIGHT, width=_CANVAS_WIDTH)


def get_coroutines() -> List[coroutine]:
    """
    Receives coroutines list.
    :return:
    """
    global COROUTINES
    return COROUTINES


def append_coroutine(new_coroutine: coroutine):
    """
    Extends coroutines list.
    :param new_coroutine: new coroutine to append
    """
    global COROUTINES
    COROUTINES.append(new_coroutine)


def get_obstacles() -> list:
    """
    Receives obstacles list.
    :return:
    """
    global OBSTACLES
    return OBSTACLES
