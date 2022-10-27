import asyncio
import time
import curses
from random import randint, choice


# stars = (
#   (3, 7),
#   (7, 6),
#   (4, 11),
#   (2, 15),
#   (10, 8),
#   (5, 3)
# )
stars = set()
stars_symbols = ['*', ':', '.', '+']


class EventLoop:
  def __await__(self):
    return (yield self)


class Sleep(EventLoop):
  def __init__(self, seconds):
    self.seconds = seconds


async def do_sleep(times_count=1):
  for _ in range(times_count):
    await Sleep(0.1)


async def change_star_stage(times_count):
  ticks = do_sleep(times_count)
  await ticks


async def blink(canvas, row, column, symbol='*'):
  symbol = choice(stars_symbols)
  while True:
    canvas.addstr(row, column, symbol, curses.A_DIM)
    await change_star_stage(10)
  
    canvas.addstr(row, column, symbol)
    await change_star_stage(3)
  
    canvas.addstr(row, column, symbol, curses.A_BOLD)
    await change_star_stage(5)
  
    canvas.addstr(row, column, symbol)
    await change_star_stage(3)


def draw(canvas):
  curses.curs_set(False)
  max_y, max_x = curses.window.getmaxyx(canvas)
  for _ in range(100):
    stars.add((randint(1, max_y-1), randint(1, max_x-1)))

  canvas.border()
  canvas.refresh()
  corutines = [blink(canvas, row, column) for row, column in stars]

  while True:
    for corutine in corutines:
      corutine.send(None)
      canvas.refresh()
      # time.sleep(0.1)
      corutine.send(None)
      canvas.refresh()
      # time.sleep(0.1)
      corutine.send(None)
      canvas.refresh()
      # time.sleep(1)
      corutine.send(None)
      canvas.refresh()
      # time.sleep(1)
      corutine.send(None)
      canvas.refresh()
    time.sleep(1)


if __name__ == '__main__':
  curses.update_lines_cols()
  curses.wrapper(draw)
