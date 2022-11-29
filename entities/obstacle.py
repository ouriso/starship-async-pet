from typing import List

from entities.space_objects import SpaceObject
from utils.canvas_dimensions import get_canvas_dimensions
from utils.frames import draw_frame
from utils.sleep import sleep


class Obstacle:

    def __init__(self, space_object: SpaceObject, uid=None):
        self.space_object = space_object
        self.uid = uid

    def __eq__(self, other):
        return other == self.space_object

    def get_bounding_box_frame(self):
        # increment box size to compensate obstacle movement
        height = self.space_object.dimensions.height + 1
        width = self.space_object.dimensions.width + 1
        return '\n'.join(_get_bounding_box_lines(height, width))

    def dump_bounding_box(self):
        start_pos_y = self.space_object.position_y - 1
        start_pos_x = self.space_object.position_x - 1
        return start_pos_y, start_pos_x, self.get_bounding_box_frame()

    def has_collision(self, another_object_top, another_object_bottom,
                      another_object_left, another_object_right) -> bool:
        top = self.space_object.object_borders().top
        bottom = self.space_object.object_borders().bottom
        left = self.space_object.object_borders().left
        right = self.space_object.object_borders().right
        is_collision = any([
            _is_point_inside(top, bottom, left, right,
                             another_object_top, another_object_left),
            _is_point_inside(top, bottom, left, right,
                             another_object_bottom, another_object_right),

            _is_point_inside(another_object_top, another_object_bottom,
                             another_object_left, another_object_right,
                             top, left),
            _is_point_inside(another_object_top, another_object_bottom,
                             another_object_left, another_object_right,
                             bottom, right)
        ])
        if is_collision:
            self.space_object.set_need_to_stop()
        return is_collision


def _is_point_inside(obstacle_top, obstacle_bottom,
                     obstacle_left, obstacle_right,
                     point_pos_y, point_pos_x) -> bool:
    rows_flag = obstacle_top <= point_pos_y < obstacle_bottom
    columns_flag = obstacle_left <= point_pos_x < obstacle_right
    return rows_flag and columns_flag


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
            elif obstacle.space_object.need_to_stop:
                continue
            boxes.append(obstacle.dump_bounding_box())

        for row, column, frame in boxes:
            draw_frame(canvas, row, column, frame)

        await sleep()

        for row, column, frame in boxes:
            draw_frame(canvas, row, column, frame, negative=True)


def check_object_collisions(
        position_y: int, position_x: int, object_height: int, object_width: int
) -> bool:
    for obstacle in get_obstacles():
        is_collision = obstacle.has_collision(
            position_y, position_y + object_height,
            position_x, position_x + object_width
        )

        if is_collision:
            return True
    return False


OBSTACLES: List[Obstacle] = []


def get_obstacles():
    global OBSTACLES
    return OBSTACLES
