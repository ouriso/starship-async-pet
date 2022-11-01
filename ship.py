import asyncio
from itertools import cycle
from frames import draw_frame, get_frame_size  #, read_controls

with open(r'./animations/ship_frame_1.txt', 'r', encoding='utf-8') as fp:
  ship_frame_1 = fp.read()
  rows_1, columns_1 = get_frame_size(ship_frame_1)
  square_1 = rows_1 * columns_1

with open(r'./animations/ship_frame_2.txt', 'r', encoding='utf-8') as fp:
  ship_frame_2 = fp.read()
  rows_2, columns_2 = get_frame_size(ship_frame_2)
  square_2 = rows_2 * columns_2

with open(r'./animations/ship.txt', 'r', encoding='utf-8') as fp:
  ship = fp.read()
  ship_rows, ship_columns = get_frame_size(ship_frame_2)

ship_frames = [
  (ship_frame_1, False),
  (ship_frame_1, True),
  (ship_frame_2, False),
  (ship_frame_2, True)
]


async def ship_animate(canvas, ship_y, ship_x):

  for ship_frame, negative in cycle(ship_frames):
    draw_frame(canvas, ship_y, ship_x, ship)
    draw_frame(canvas, ship_y + ship_rows + rows_1, ship_x, ship_frame, negative)
    await asyncio.sleep(0)
