import time
import curses
import asyncio
import curses
import random


def draw(canvas):
    row, column = (5, 20)
    canvas.addstr(row, column, 'Hello, World!', curses.A_REVERSE | curses.A_BLINK)
    canvas.border()
    curses.curs_set(False)
    canvas.refresh()
    time.sleep(4)


def draw_star(canvas):
    curses.curs_set(False)
    row, column = (3, 10)
    canvas.addstr(row, column, '*', curses.A_DIM)
    time.sleep(2)
    canvas.refresh()
    canvas.addstr(row, column, '*')
    time.sleep(0.3)
    canvas.refresh()
    canvas.addstr(row, column, '*', curses.A_BOLD)
    time.sleep(0.5)
    canvas.refresh()
    canvas.addstr(row, column, '*')
    time.sleep(0.3)
    canvas.refresh()


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


def choose_star():
  stars = ['+', ':', '*', '.']
  return random.choice(stars)


def choose_coords(maxx, maxy):
  return random.randint(1, maxx-1), random.randint(1, maxy-1)


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await Sleep(2)

        canvas.addstr(row, column, symbol)
        await Sleep(0.3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await Sleep(0.5)

        canvas.addstr(row, column, symbol)
        await Sleep(0.3)


def main(canvas):
    curses.curs_set(False)
    stars_count = 100
    coroutines = []
    canvas_width, canvas_height = canvas.getmaxyx()
    for star in range(stars_count):
        row, column = choose_coords(canvas_width, canvas_height)
        coroutines.append(blink(canvas, row, column, symbol=choose_star()))
    iterations_before_change_brightness = [0]*(stars_count+1)
    gun_shot = fire(canvas, 18, 30)
    coroutines.append(gun_shot)
    while True:
      try:
        for num, coroutine in enumerate(coroutines):
          if iterations_before_change_brightness[num] <= 0:
            try:
              seconds_to_sleep = coroutines[random.randint(0,len(coroutines)-1)].send(None).seconds
            except AttributeError:
              seconds_to_sleep = 1
            ticks_to_sleep = convert_seconds_to_iterations(
              seconds_to_sleep
            )
            iterations_before_change_brightness[num] = ticks_to_sleep
          iterations_before_change_brightness[num] -= 1
      except StopIteration:
            coroutines.remove(coroutine)
      if len(coroutines) == 0:
        break
      canvas.refresh()


class EventLoopCommand():

    def __await__(self):
        return (yield self)


class Sleep(EventLoopCommand):

  def __init__(self, seconds):
      self.seconds = seconds


def convert_seconds_to_iterations(seconds):
  return seconds * 10000


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
    #curses.wrapper(draw)
    #while True:
        #curses.wrapper(draw_star)
