from typing import List, Tuple

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

    def get_bounding_box_frame(self) -> str:
        """
        Generates a rectangular box surrounding the current object.
        :return: string as a rectangular box
        """
        # increment box size to compensate obstacle movement
        height = self.space_object.dimensions.height + 1
        width = self.space_object.dimensions.width + 1
        return '\n'.join(_get_bounding_box_lines(height, width))

    def dump_bounding_box(self) -> Tuple[int, int, str]:
        """
        Defines the initial position of the box surrounding the current object.
        :return: tuple of initial y and x-axes and rectangular box string
        """
        start_pos_y = self.space_object.position_y - 1
        start_pos_x = self.space_object.position_x - 1
        return start_pos_y, start_pos_x, self.get_bounding_box_frame()

    def has_collision(self, another_object_top, another_object_bottom,
                      another_object_left, another_object_right) -> bool:
        """
        Checks if obstacle has collision with other object.
        :param another_object_top: y-coord of the object's upper left corner
        :param another_object_bottom: y-coord of the object's lower right corner
        :param another_object_left: x-coord of the object's upper left corner
        :param another_object_right: x-coord of the object's lower right corner
        :return: True - if there is a collision, else - False
        """
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
            # if there is a collision - the obstacle must be exploded
            self.space_object.set_need_to_stop()
        return is_collision


def _is_point_inside(obstacle_top, obstacle_bottom,
                     obstacle_left, obstacle_right,
                     point_pos_y, point_pos_x) -> bool:
    rows_flag = obstacle_top <= point_pos_y < obstacle_bottom
    columns_flag = obstacle_left <= point_pos_x < obstacle_right
    return rows_flag and columns_flag


def _get_bounding_box_lines(height, width) -> str:
    """
    Returns a rectangular box surrounding the object
     with sizes height and width.
    :param height: height of object to surround
    :param width: width of object to surround
    :return: string as a rectangular box
    """
    yield ' ' + '-' * width + ' '
    for _ in range(height):
        yield '|' + ' ' * width + '|'
    yield ' ' + '-' * width + ' '


async def show_obstacles(canvas, obstacles: List[Obstacle]):
    """
    Display bounding boxes of every obstacle in a list.
    """
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
    """
    Checks if object has collision with any obstacle.
    :return: True - if there is a collision, else - False
    :param position_y: y-coord of the object's upper left corner
    :param position_x: x-coord of the object's upper left corner
    :param object_height: height of the object
    :param object_width: width of the object
    :return: True - if there is a collision, else - False
    """
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
