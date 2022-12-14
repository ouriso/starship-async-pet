from abc import ABC, abstractmethod
from random import randrange

from utils.globals import get_obstacles, get_canvas_dimensions
from utils.sleep import sleep


class Gun(ABC):
    """
    Abstract class that implements the firing of weapons
    installed on the starship.
    """
    delay = 0

    async def fire(
            self, canvas,
            start_position_y: int, start_position_x: int,
    ):
        await self.animate_flash(canvas, start_position_y, start_position_x)
        await self.animate_bullet(canvas, start_position_y, start_position_x)

    @staticmethod
    async def animate_flash(
            canvas, start_position_y: int, start_position_x: int
    ):
        """
        Gun charging animation.
        :param canvas: current WindowObject
        :param start_position_y: charging start position on y-axis
        :param start_position_x: charging start position on x-axis
        """
        canvas.addstr(round(start_position_y), round(start_position_x), '*')
        await sleep()
        canvas.addstr(round(start_position_y), round(start_position_x), 'O')
        await sleep()
        canvas.addstr(round(start_position_y), round(start_position_x), ' ')

    @abstractmethod
    async def animate_bullet(self, canvas, position_y: int, position_x: int):
        """
        Bullet moving animation.
        :param canvas: current WindowObject
        :param position_y: bullet start position on y-axis
        :param position_x: bullet start position on x-axis
        :return:
        """


class OldTroopersBlaster(Gun):
    """
    Single-shot blaster with randomly generated firing direction.
    """
    async def animate_bullet(self, canvas, position_y: int, position_x: int):
        # random generation of the bullet direction
        y_speed = randrange(-20, 0, 1) / 10
        x_speed = randrange(-5, 5, 1) / 10
        symbol = self.get_bullet_symbol_by_direction(y_speed, x_speed)
        height, width = get_canvas_dimensions()
        bullet_y = position_y + y_speed
        bullet_x = position_x + x_speed

        while 0 < bullet_y < height and 0 < bullet_x < width:
            canvas.addstr(round(bullet_y), round(bullet_x), symbol)
            await sleep(2)
            canvas.addstr(round(bullet_y), round(bullet_x), ' ')
            bullet_y += y_speed
            bullet_x += x_speed

            for obstacle in get_obstacles():
                is_collision = obstacle.has_collision(
                    bullet_y, bullet_y + 1,
                    bullet_x, bullet_x + 1
                )

                if is_collision:
                    return

    @staticmethod
    def get_bullet_symbol_by_direction(y_speed: float, x_speed: float) -> str:
        """
        Changes bullet symbol depending on direction.
        :param y_speed: moving speed by y-direction
        :param x_speed: moving speed by x-direction
        :return: symbol
        """
        # 1.6 and 0.6 are experimentally calculated ratios of y_ and x_speed
        # indicating that the bullet symbol needs to be changed
        if not x_speed or abs(y_speed) > 1.6 * abs(x_speed):
            symbol = '|'
        elif not y_speed or abs(y_speed) < 0.6 * abs(x_speed):
            symbol = '-'
        elif (y_speed * x_speed) > 0:
            symbol = '\\'
        else:
            symbol = '/'
        return symbol
