from json import load

from config import GAME_YEAR_DURATION
from utils.globals import append_coroutine
from utils.frames import update_frame
from utils.sleep import calculate_ticks_number

YEAR = 1957
PHRASES = {
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Take the plasma gun! Shoot the garbage!",
}


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


def generate_text_from_number(number: int) -> str:
    """
    Generate text representation of integer number.
    :param number: any number
    :return: text representation of passed number
    """
    with open('./animations/numbers.json', 'r') as fp:
        numbers = load(fp)
    text = zip(*[numbers[num].split('\n') for num in str(number)])
    text = '\n'.join([''.join(line) for line in list(text)])
    return text


async def create_phrase(derive_canvas):
    """
    Generates sentences describing what's special
    about current game year for space.
    :param derive_canvas: current derived WindowObject
    """
    ticks = calculate_ticks_number(1.5)
    pos_y, pos_x = (5, 0)

    famous_year = PHRASES.get(get_current_year(), '')
    await update_frame(derive_canvas, pos_y, pos_x, famous_year, ticks)


async def animate_year(derive_canvas):
    """
    Animates current game year changing.
    :param derive_canvas: current derived WindowObject
    """
    ticks = calculate_ticks_number(GAME_YEAR_DURATION)
    while True:
        text_year = generate_text_from_number(get_current_year())

        append_coroutine(create_phrase(derive_canvas))
        await update_frame(derive_canvas, 0, 0, text_year, ticks)

        increment_year()
        derive_canvas.refresh()
