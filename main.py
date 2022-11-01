import time
import curses
from random import randint, randrange
from gun import fire
from ship import ship_animate
from stars import blink, generate_stars

with open(r'./animations/ship_frame_1.txt', 'r', encoding='utf-8') as fp:
  ship_frame_1 = fp.read()

with open(r'./animations/ship_frame_2.txt', 'r', encoding='utf-8') as fp:
  ship_frame_2 = fp.read()
ship_frames = [ship_frame_1, ship_frame_2]


def draw(canvas):
  curses.curs_set(False)
  max_y, max_x = curses.window.getmaxyx(canvas)

  start_pos = (
    max_y * 3 / 4, max_x / 2
  )
  
  stars = generate_stars(max_y, max_x)

  canvas.border()
  canvas.refresh()
  corutines = [
    fire(
      canvas, start_pos[0] - 1, start_pos[1] + 2, 
      randrange(-10, 10, 1) / 10, randrange(-10, 10, 1) / 10
    )
  ]
  corutines_add = [blink(canvas, row, column, randint(10, 70)) for row, column in stars]
  corutines_add.append(ship_animate(canvas, *start_pos))

  while True:
    corutines.extend(corutines_add)
    for corutine in corutines.copy():
      try:
        corutine.send(None)
        canvas.refresh()
      except StopIteration:
        corutines.remove(corutine)
        continue
    
    time.sleep(0.2)


if __name__ == '__main__':
  curses.update_lines_cols()
  curses.wrapper(draw)
