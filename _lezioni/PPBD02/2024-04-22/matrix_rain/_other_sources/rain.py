#!/usr/bin/env python3
# pylint: disable=missing-docstring
import os, curses, random, time

# CGREEN2 terminal color 
CGREEN2  = "\33[92m"

# half-width katakana unicode range
KATAKANA = [chr(c) for c in range(0xff67, 0xff9e)]
PUNCT_MARKS = ['-', '*', '&', '#', '@', '&', '$']
NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

class Matrix(object):
    def __init__(self, chance_on=0.95, chance_off=0.90, delay=0.050):
        self.charset = KATAKANA + PUNCT_MARKS + NUMBERS
        self.delay = delay
        self.is_live = []
        self.chance_on = chance_on
        self.chance_off = chance_off

    def enter(self, stdscr):
        curses.has_colors()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.curs_set(0)
        stdscr.idlok(1)

        while True:
            start = time.time()
            self.rain(stdscr)
            stdscr.refresh()
            elapsed = time.time() - start
            time.sleep(max([0, self.delay - elapsed]))

    def new_line(self, stdscr):
        color = curses.color_pair(1)

        for column, live in enumerate(self.is_live):
            roll = random.random()
            attr = color

            if not live and roll > self.chance_on:
                live = True
                self.is_live[column] = True
                attr = color | curses.A_REVERSE
            elif live and roll > self.chance_off:
                self.is_live[column] = False
                attr = color | curses.A_DIM

            if live:
                stdscr.addch(random.choice(self.charset), attr)
            else:
                stdscr.addch(' ')

    def rain(self, stdscr):
        (dummy, columns) = stdscr.getmaxyx()

        if len(self.is_live) != columns:
            self.is_live = [False] * columns

        stdscr.move(0, 0)
        stdscr.insertln()
        self.new_line(stdscr)

def main():
    matrix = Matrix()

    print(CGREEN2 + "Wake up, Neo...")
    time.sleep(2)

    # clear terminal before enter in the Matrix
    os.system('cls' if os.name == 'nt' else 'clear')

    curses.wrapper(matrix.enter)

if __name__ == '__main__':
    main()