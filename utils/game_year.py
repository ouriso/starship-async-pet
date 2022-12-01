from json import load

from utils.frames import update_frame
from utils.sleep import calculate_ticks_number

YEAR = 1957


def increment_year():
    """
    Increments year by 1.
    """
    global YEAR
    YEAR += 1


def get_current_year() -> int:
    """
    Returns current year value.
    """
    global YEAR
    return YEAR


with open('./animations/numbers.json', 'r') as fp:
    numbers = load(fp)


def generate_text_year(year: int):
    text = zip(*[numbers[num].split('\n') for num in str(year)])
    text = '\n'.join([''.join(line) for line in list(text)])
    return text


async def animate_year(canvas):
    ticks = calculate_ticks_number(1.5)
    while True:
        text_year = generate_text_year(get_current_year())
        await update_frame(canvas, 1, 1, text_year, ticks)
        increment_year()
