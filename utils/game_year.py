from json import load

from utils.frames import update_frame

with open('./animations/numbers.json', 'r') as fp:
    numbers = load(fp)


def generate_text_year(year: int):
    text = zip(*[numbers[num].split('\n') for num in str(year)])
    text = '\n'.join([''.join(line) for line in list(text)])
    return text


async def animate_year(canvas):
    year = 1957
    while True:
        text_year = generate_text_year(year)
        await update_frame(canvas, 1, 1, text_year, 100)
        year += 1
