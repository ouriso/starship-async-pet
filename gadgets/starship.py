import math
from itertools import cycle
from types import coroutine

from config import ROWS_SPEED_LIMIT, COLUMNS_SPEED_LIMIT, ITS_A_GUN_TIME
from controls import read_controls
from entities.obstacle import check_object_collisions
from entities.space_objects import SpaceObject
from gadgets.guns import OldTroopersBlaster
from utils.globals import append_coroutine, get_canvas_dimensions
from utils.frames import update_frame
from utils.game_over import game_over_animate
from utils.game_year import get_current_year
from utils.sleep import sleep


class BaseStarShip(SpaceObject):
    """
    Implements the positioning of a starship in the current window.
    """
    frame_lifetime = 2
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

            await update_frame(canvas, pos_y, pos_x, frame, self.frame_lifetime)

            if self.need_to_stop:
                return

    async def run_starship(self, canvas):
        append_coroutine(self.animate(canvas))
        while True:
            rows_direction, columns_direction, need_fire = read_controls(canvas)
            self.change_position(rows_direction, columns_direction)
            if (get_current_year() > ITS_A_GUN_TIME) and need_fire:
                append_coroutine(self.fire(canvas))
            await sleep()
            if check_object_collisions(
                self.position_y, self.position_x, *self.dimensions
            ):
                break

        # if collision was happened stop ship animation, explode and game_over
        self.set_need_to_stop()
        await self.explode(canvas)
        append_coroutine(game_over_animate(canvas))

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
        """Change speed ??? accelerate or brake ??? according to force direction."""

        speed_fraction = current_speed / speed_limit

        # if the ship is stationary - accelerate quickly
        # if the ship is already flying fast - accelerate slowly
        delta = math.cos(speed_fraction) * 0.75

        result_speed = current_speed + delta * speed_direction

        result_speed = self._limit(result_speed, speed_limit)

        # ???????? ???????????????? ???????????? ?? ????????, ???? ?????????????????????????? ??????????????
        if abs(result_speed) < 0.1:
            result_speed = 0

        return result_speed

    def update_speed(self, rows_direction, columns_direction):
        """
        Update speed smoothly to make control handy for player.
        Set up a new speed value (row_speed, column_speed).

        :param rows_direction: is a direction by y-axis
        :param columns_direction: is a direction by x-axis
         ??? Possible values for both params:
           -1 ??? pulls up (rows_direction) or left (columns_direction)
           0  ??? has no effect
           1  ??? pulls down (rows_direction) or right (columns_direction)
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

        # ?????????? ????????????????, ?????????? ?????????????? ???????????????????????????? ???? ????????????????
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

        # TODO ???????????? ????????????????????????
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
