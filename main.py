import time
import curses
import asyncio
import curses
import random

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
'''

def choose_star():
  stars = ['+', ':', '*', '.']
  return random.choice(stars)


def choose_coords(maxx, maxy):
  return random.randint(1, maxx-1), random.randint(1, maxy-1)


def main(canvas):
    canvas.border()
    curses.curs_set(False)
    stars_count = 100
    coroutines = []
    max_row, max_column = canvas.getmaxyx()
    coroutine = blink(canvas, 5, 5)
    for i in range(stars_count):
        coroutines.append(blink(
            canvas,
            random.randint(2, max_row-2),
            random.randint(2, max_column-2),
            symbol=choose_star()
        ))
    x = 0
    while x<10000:
        x += 1
        try:
            coroutine_num = random.randint(0,len(coroutines)-1)
            coroutines[coroutine_num].send(None)
        #for coroutine in coroutines:
            #coroutine.send(None)
        except StopIteration:
            coroutines.remove(coroutines[coroutine_num])
        canvas.refresh()
        time.sleep(0.01)


async def blink(canvas, row, column, symbol='*'):
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(10):
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
