import time
import curses
import asyncio
import curses
import random
import sys
from curses_tools import read_controls, draw_frame, get_frame_size


'''
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
'''


def get_frame(file_path):
    with open(file_path, 'r') as file:
        return file.read()


async def animate_spaceship(canvas, frame_1, frame_2, row, column):
    while True:
        draw_frame(canvas, row, column, frame_1)
        for _ in range(2):
            await asyncio.sleep(0)

        draw_frame(canvas, row, column, frame_1, negative=True)

        draw_frame(canvas, row, column, frame_2)
        for _ in range(2):
            await asyncio.sleep(0)

        draw_frame(canvas, row, column, frame_2, negative=True)


async def control_spaceship(canvas, row, column, frame_1, frame_2):
    rows_direction, columns_direction, space_pressed = read_controls(canvas)
    canvas.addstr(5,5, str(rows_direction))
    spaceship = animate_spaceship(canvas,
                                  frame_1,
                                  frame_2,
                                  row+rows_direction,
                                  column+ columns_direction)
    await spaceship


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


def main(canvas):
    canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)
    stars_count = 100
    coroutines = []
    max_row, max_column = canvas.getmaxyx()
    gun_shot = fire(canvas, max_row-2, max_column//2)
    for _ in range(stars_count):
        coroutines.append(blink(
            canvas,
            random.randint(2, max_row-2),
            random.randint(2, max_column-2),
            symbol=choose_star()
        ))
    x = 0
    frame_1 = get_frame('./animations/rocket_frame_1.txt')
    frame_2 = get_frame('./animations/rocket_frame_2.txt')
    spaceship_width, spaceship_height = get_frame_size(frame_1)
    spaceship = control_spaceship(canvas,
                                  (max_row//2-spaceship_width//2),
                                  (max_column//2 - spaceship_height//2),
                                  frame_1,
                                  frame_2)
    while x<500:
        x += 1
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        for _ in range(stars_count):
            coroutine = random.choice(coroutines)
            coroutine.send(None)
        try:
            gun_shot.send(None)
        except StopIteration:
            pass
        except RuntimeError:
            canvas.clear()
            canvas.addstr(max_row//2,
                          (max_column//2 - 11),
                          "Rocket's been launched!",
                          curses.A_BOLD)
            canvas.refresh()
            time.sleep(3)
            sys.exit()
        spaceship.send(None)
        canvas.refresh()
        time.sleep(0.1)


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
