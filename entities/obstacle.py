from typing import List

from entities.space_objects import SpaceObject
from utils.canvas_dimensions import get_canvas_dimensions
from utils.frames import draw_frame
from utils.sleep import sleep


class Obstacle:

    def __init__(self, space_object: SpaceObject, uid=None):
        self.space_object = space_object
        self.uid = uid

    def get_bounding_box_frame(self):
        # increment box size to compensate obstacle movement
        height = self.space_object.dimensions.height + 1
        width = self.space_object.dimensions.width + 1
        return '\n'.join(_get_bounding_box_lines(height, width))

    def dump_bounding_box(self):
        start_pos_y = self.space_object.position_y - 1
        start_pos_x = self.space_object.position_x - 1
        return start_pos_y, start_pos_x, self.get_bounding_box_frame()


def _get_bounding_box_lines(height, width):
    yield ' ' + '-' * width + ' '
    for _ in range(height):
        yield '|' + ' ' * width + '|'
    yield ' ' + '-' * width + ' '


async def show_obstacles(canvas, obstacles: List[Obstacle]):
    """Display bounding boxes of every obstacle in a list"""
    height, width = get_canvas_dimensions()

    while True:
        boxes = []

        for obstacle in obstacles:
            if obstacle.space_object.position_y >= height:
                continue
            boxes.append(obstacle.dump_bounding_box())

        for row, column, frame in boxes:
            draw_frame(canvas, row, column, frame)

        await sleep()

        for row, column, frame in boxes:
            draw_frame(canvas, row, column, frame, negative=True)
