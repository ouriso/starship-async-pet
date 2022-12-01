from json import load

from utils.event_loop import append_coroutine
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


with open('./animations/numbers.json', 'r') as fp:
    numbers = load(fp)


def generate_text_year(year: int):
    text = zip(*[numbers[num].split('\n') for num in str(year)])
    text = '\n'.join([''.join(line) for line in list(text)])
    return text


async def create_phrase(derive_canvas):
    ticks = calculate_ticks_number(1.5)
    pos_y, pos_x = (5, 0)

    famous_year = PHRASES.get(get_current_year(), '')
    await update_frame(derive_canvas, pos_y, pos_x, famous_year, ticks)


async def animate_year(derive_canvas):
    ticks = calculate_ticks_number(1.5)
    while True:
        text_year = generate_text_year(get_current_year())

        append_coroutine(create_phrase(derive_canvas))
        await update_frame(derive_canvas, 0, 0, text_year, ticks)

        increment_year()
        derive_canvas.refresh()
