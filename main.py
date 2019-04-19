import time
import curses
import asyncio
import curses
import random
import sys
from curses_tools import read_controls, draw_frame, get_frame_size



def get_frame(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def is_crossing_border(current_position ,shift_direction,
                       frame_length, canvas_size):
    space_near_border = 1
    critical_position = canvas_size - frame_length - space_near_border
    return ((current_position < critical_position) and (shift_direction > 0))\
           or ((current_position > space_near_border) and (shift_direction < 0))


async def animate_spaceship(canvas, frame_1, frame_2, row, column):
    while True:
        frames = [frame_1, frame_2]
        for frame in frames:
            maxx, maxy = canvas.getmaxyx()
            rows_direction, columns_direction, space_direction = read_controls(canvas)
            frame_rows, frame_columns = get_frame_size(frame)

            if is_crossing_border(row, rows_direction, frame_rows, maxx):
                row += rows_direction
            if is_crossing_border(column, columns_direction, frame_columns, maxy):
                column += columns_direction

            draw_frame(canvas, row, column, frame)
            await asyncio.sleep(0)

            draw_frame(canvas, row, column, frame, negative=True)


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


def main(canvas):
    canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)
    stars_count = 100
    coroutines = []
    max_row, max_column = canvas.getmaxyx()
    space_near_border = 2
    for _ in range(stars_count):
        coroutines.append(blink(
            canvas,
            random.randint(space_near_border, max_row-space_near_border),
            random.randint(space_near_border, max_column - space_near_border),
            symbol=choose_star()
        ))
    frame_1 = get_frame('./animations/rocket_frame_1.txt')
    frame_2 = get_frame('./animations/rocket_frame_2.txt')
    spaceship_width, spaceship_height = get_frame_size(frame_1)
    rows_center = max_row//2-spaceship_width//2
    columns_center = max_column//2 - spaceship_height//2
    spaceship = animate_spaceship(canvas,
                                  frame_1,
                                  frame_2,
                                  rows_center,
                                  columns_center)
    coroutines.append(spaceship)
    loop = 0
    loops_count = 100
    while loop < loops_count:
        loop += 1
        for coroutine in coroutines:
            coroutine.send(None)
        canvas.refresh()
        time.sleep(0.1)


async def blink(canvas, row, column, symbol='*'):
    while True:
        for _ in range(random.randint(1,20)):
            await asyncio.sleep(0)

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
