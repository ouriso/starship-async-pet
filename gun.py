import curses

from config import BASE_DELAY
from utils.sleep import Sleep


async def fire(
    canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0
):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await Sleep(BASE_DELAY)
    canvas.addstr(round(row), round(column), 'O')
    await Sleep(BASE_DELAY)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    if columns_speed == 0 or abs(rows_speed) > 1.6 * abs(columns_speed):
        symbol = '|'
    elif rows_speed == 0 or abs(rows_speed) < 0.6 * abs(columns_speed):
        symbol = '-'
    elif (rows_speed * columns_speed) > 0:
        symbol = '\\'
    else:
        symbol = '/'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows, columns

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await Sleep(BASE_DELAY)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed
