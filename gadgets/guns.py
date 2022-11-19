from abc import ABC, abstractmethod
from random import randrange

from config import BASE_DELAY
from utils.canvas_dimensions import get_canvas_dimensions
from utils.sleep import sleep


class Gun(ABC):
    delay = 0

    async def fire(
            self, canvas,
            start_position_y: int, start_position_x: int,
    ):
        await self.flash_style(canvas, start_position_y, start_position_x)
        await self.bullet_moving(canvas, start_position_y, start_position_x)

    @staticmethod
    async def flash_style(
            canvas, start_position_y: int, start_position_x: int
    ):
        """
        Gun charging animation.
        :param canvas: current WindowObject
        :param start_position_y: charging start position on y-axis
        :param start_position_x: charging start position on x-axis
        """
        canvas.addstr(round(start_position_y), round(start_position_x), '*')
        await sleep(BASE_DELAY / 2)
        canvas.addstr(round(start_position_y), round(start_position_x), 'O')
        await sleep(BASE_DELAY / 2)
        canvas.addstr(round(start_position_y), round(start_position_x), ' ')

    @abstractmethod
    async def bullet_moving(self, canvas, position_y: int, position_x: int):
        """
        Bullet moving animation.
        :param canvas: current WindowObject
        :param position_y: bullet start position on y-axis
        :param position_x: bullet start position on x-axis
        :return:
        """
        pass


class OldTroopersBlaster(Gun):
    """
    Single-shot blaster with randomly generated firing direction.
    """
    async def bullet_moving(self, canvas, position_y: int, position_x: int):
        y_speed = randrange(-20, 0, 1) / 10
        x_speed = randrange(-5, 5, 1) / 10
        symbol = self.bullet_symbol(y_speed, x_speed)
        height, width = get_canvas_dimensions()
        bullet_y = position_y + round(y_speed)
        bullet_x = position_x + round(x_speed)

        while 0 < bullet_y < height and 0 < bullet_x < width:
            canvas.addstr(round(bullet_y), round(bullet_x), symbol)
            await sleep(BASE_DELAY)
            canvas.addstr(round(bullet_y), round(bullet_x), ' ')
            bullet_y += y_speed
            bullet_x += x_speed

    @staticmethod
    def bullet_symbol(y_speed: float, x_speed: float) -> str:
        """
        Changes bullet symbol depending on direction.
        :param y_speed: moving speed by y-direction
        :param x_speed: moving speed by x-direction
        :return: symbol
        """
        if x_speed == 0 or abs(y_speed) > 1.6 * abs(x_speed):
            symbol = '|'
        elif y_speed == 0 or abs(y_speed) < 0.6 * abs(x_speed):
            symbol = '-'
        elif (y_speed * x_speed) > 0:
            symbol = '\\'
        else:
            symbol = '/'
        return symbol
