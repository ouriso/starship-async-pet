from abc import ABC, abstractmethod
from random import randrange

from config import BASE_DELAY
from gadgets.starship import StarShip
from utils.canvas_params import get_border_params
from utils.sleep import Sleep


class Gun(ABC):
    delay = 0
    y_speed: float = -0.3
    x_speed: float = 0

    def __init__(self, ship: StarShip):
        self.starship = ship

    async def fire(
            self, canvas,
            start_row: int, start_column: int,
            y_speed: float = -0.3, x_speed: float = 0
    ):
        await self.flash_style(canvas)
        await self.bullet_moving(canvas)

    @abstractmethod
    async def flash_style(self, canvas):
        pass

    @abstractmethod
    async def bullet_moving(self, canvas):
        pass


class OldTroopersBlaster(Gun):
    async def flash_style(self, canvas):
        start_position_y, start_position_x = self.starship.current_position

        canvas.addstr(round(start_position_y), round(start_position_x), '*')
        await Sleep(BASE_DELAY / 2)
        canvas.addstr(round(start_position_y), round(start_position_x), 'O')
        await Sleep(BASE_DELAY / 2)
        canvas.addstr(round(start_position_y), round(start_position_x), ' ')

    async def bullet_moving(self, canvas):
        y_speed = randrange(-10, 0, 1) / 10
        x_speed = randrange(-10, 0, 10) / 10
        symbol = self.bullet_symbol(y_speed, x_speed)
        max_y, max_x = get_border_params()
        bullet_y = self.starship.position_y + round(y_speed)
        bullet_x = (
            self.starship.position_x
            + round(self.starship.size.width / 2)
            + round(x_speed)
        )

        while 0 < bullet_y < max_y and 0 < bullet_x < max_x:
            canvas.addstr(round(bullet_y), round(bullet_x), symbol)
            await Sleep(BASE_DELAY)
            canvas.addstr(round(bullet_y), round(bullet_x), ' ')
            bullet_y += y_speed
            bullet_x += x_speed

    @staticmethod
    def bullet_symbol(y_speed: float, x_speed: float):
        if x_speed == 0 or abs(y_speed) > 1.6 * abs(x_speed):
            symbol = '|'
        elif y_speed == 0 or abs(y_speed) < 0.6 * abs(x_speed):
            symbol = '-'
        elif (y_speed * x_speed) > 0:
            symbol = '\\'
        else:
            symbol = '/'
        return symbol
