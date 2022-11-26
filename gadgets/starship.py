import math
from itertools import cycle
from types import coroutine

from config import ROWS_SPEED_LIMIT, COLUMNS_SPEED_LIMIT
from controls import read_controls
from entities.space_objects import SpaceObject
from gadgets.guns import OldTroopersBlaster
from utils.canvas_dimensions import get_canvas_dimensions
from utils.event_loop import append_coroutine
from utils.frames import draw_frame
from utils.sleep import sleep


class BaseStarShip(SpaceObject):
    """
    Implements the positioning of a starship in the current window.
    """
    frame_lifetime = 4
    speed_fading = 0.8
    speed_limit_y = ROWS_SPEED_LIMIT
    speed_limit_x = COLUMNS_SPEED_LIMIT
    gun = OldTroopersBlaster()

    def fire(self, canvas) -> coroutine:
        """
        Creates coroutine with shot animation.
        :param canvas: current WindowObject
        :return: animation of firing
        """
        # the shooting animation starts at the top of the ship
        # and in the middle of its width
        fire_routine = self.gun.fire(
            canvas, self.position_y,
            self.position_x + round(self.dimensions.width / 2)
        )
        return fire_routine

    async def animate(self, canvas) -> None:
        """
        Animates ship moving.
        :param canvas: current WindowObject
        :return:
        """
        for frame in cycle(self.frames):
            # saving the current position to prevent incorrect erasing
            pos_y = self.position_y
            pos_x = self.position_x
            draw_frame(canvas, pos_y, pos_x, frame)
            await sleep(self.frame_lifetime)
            draw_frame(canvas, pos_y, pos_x, frame, True)

    async def run_starship(self, canvas):
        append_coroutine(self.animate(canvas))
        while True:
            rows_direction, columns_direction, need_fire = read_controls(canvas)
            self.change_position(rows_direction, columns_direction)
            if need_fire:
                append_coroutine(self.fire(canvas))
            await sleep()

    @staticmethod
    def _limit(value, speed_limit: int):
        """Limit value by min_value and max_value."""

        if value < -speed_limit:
            return -speed_limit
        if value > speed_limit:
            return speed_limit
        return value

    def _apply_acceleration(self, current_speed: float,
                            speed_limit: int, speed_direction: int):
        """Change speed — accelerate or brake — according to force direction."""

        speed_fraction = current_speed / speed_limit

        # если корабль стоит на месте, дергаем резко
        # если корабль уже летит быстро, прибавляем медленно
        delta = math.cos(speed_fraction) * 0.75

        result_speed = current_speed + delta * speed_direction

        result_speed = self._limit(result_speed, speed_limit)

        # если скорость близка к нулю, то останавливаем корабль
        if abs(result_speed) < 0.1:
            result_speed = 0

        return result_speed

    def update_speed(self, rows_direction, columns_direction):
        """
        Update speed smoothly to make control handy for player.
        Return new speed value (row_speed, column_speed).

        rows_direction — is a force direction by y-axis. Possible values:
           -1 — if force pulls up
           0  — if force has no effect
           1  — if force pulls down
        columns_direction — is a force direction by x-axis. Possible values:
           -1 — if force pulls left
           0  — if force has no effect
           1  — if force pulls right
        """

        if rows_direction not in (-1, 0, 1):
            raise ValueError(
                f'Wrong rows_direction value {rows_direction}.'
                f' Expects -1, 0 or 1.'
            )

        if columns_direction not in (-1, 0, 1):
            raise ValueError(
                f'Wrong columns_direction value {columns_direction}.'
                f' Expects -1, 0 or 1.'
            )

        # гасим скорость, чтобы корабль останавливался со временем
        self.speed_by_y *= self.speed_fading
        self.speed_by_x *= self.speed_fading

        if rows_direction:
            self.speed_by_y = self._apply_acceleration(
                self.speed_by_y, self.speed_limit_y, rows_direction
            )

        if columns_direction:
            self.speed_by_x = self._apply_acceleration(
                self.speed_by_x, self.speed_limit_x, columns_direction
            )

    def change_position(
            self, rows_direction: int, columns_direction: int) -> None:
        """
        Changes the position of the object depending on the offset arguments
        and maximum available offset values.
        :param rows_direction: y-axis offset direction
        :param columns_direction: x-axis offset direction
        :return:
        """
        height, width = get_canvas_dimensions()
        min_y = min_x = 1
        self.update_speed(rows_direction, columns_direction)

        object_borders = self.object_borders()

        # TODO убрать дублирование
        if self.speed_by_y < 0:
            self.speed_by_y = max(self.speed_by_y, min_y - object_borders.top)
        elif self.speed_by_y > 0:
            self.speed_by_y = min(self.speed_by_y,
                                  height - object_borders.bottom)
        if self.speed_by_x < 0:
            self.speed_by_x = max(self.speed_by_x, min_x - object_borders.left)
        elif self.speed_by_x > 0:
            self.speed_by_x = min(self.speed_by_x, width - object_borders.right)

        self.position_y += self.speed_by_y
        self.position_x += self.speed_by_x
