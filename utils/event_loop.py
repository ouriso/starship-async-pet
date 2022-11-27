from types import coroutine
from typing import List

from entities.obstacle import Obstacle

COROUTINES: List[coroutine] = []
OBSTACLES: List[Obstacle] = []


def get_coroutines():
    global COROUTINES
    return COROUTINES


def append_coroutine(new_coroutine: coroutine):
    global COROUTINES
    COROUTINES.append(new_coroutine)


def delete_coroutine(exhaustion_coroutine):
    global COROUTINES
    COROUTINES.remove(exhaustion_coroutine)


def get_obstacles():
    global OBSTACLES
    return OBSTACLES
