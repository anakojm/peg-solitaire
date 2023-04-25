#!/usr/bin/env python3
"""
This is a game of peg solitaire in python
The goal of the game is to empty the board except for one center peg
To reach that goal you can move a piece, you can only move a piece by "jumping"
over another one, "eating" it in the process. The destination must be empty.
· indicates a peg in a hole, * emboldened indicates the peg to be moved,
and o indicates an empty hole. A blue ¤ is the hole the current peg moved from;
a red * is the final position of that peg,
a red o is the hole of the peg that was jumped and removed.
TODO: Remove dependencies
TODO: add type hints
TODO: use wikipedia's syntax to input moves
"""
import atexit
from os import name, system, getcwd
from pickle import Pickler, Unpickler
from typing import NamedTuple, Callable
from copy import deepcopy
from enum import Enum, auto
from getkey import getkey, keys



class Action(Enum):
    SELECT = auto()
    LEFT = auto()
    DOWN = auto()
    UP = auto()
    RIGHT = auto()
    SAVE = auto()
    LOAD = auto()
    QUIT = auto()

BINDS = {
    keys.ENTER: Action.SELECT,
    keys.SPACE: Action.SELECT,

    keys.LEFT: Action.LEFT,
    keys.DOWN: Action.DOWN,
    keys.UP: Action.UP,
    keys.RIGHT: Action.RIGHT,

    "h": Action.LEFT,
    "j": Action.DOWN,
    "k": Action.UP,
    "l": Action.RIGHT,

    keys.ESCAPE: Action.QUIT,
    "q": Action.QUIT,
    "m": Action.QUIT,

    "s": Action.SAVE,
    "J": Action.SAVE,

    "L": Action.LOAD,
}



class Tile(Enum):
    HOLE = auto()
    PEG = auto()

class Board(NamedTuple):
    tiles: list
    width: int

class Game(NamedTuple):
    board: Board
    won: Callable
    minimum_moves: int



def str_to_tile(str):
    return {
        " ": None,
        "0": Tile.HOLE,
        "1": Tile.PEG,
    }[str]



def pad_right(list, length, element):
    return list + [element] * (length - len(list))

def str_to_board(str):
    lines = str.splitlines()

    tiles = []
    width = max([len(line) for line in lines])

    for line in lines:
        tiles += pad_right([str_to_tile(char) for char in line], width, None)

    return Board(tiles, width)



def last_peg(board):
    index = board.tiles.index(Tile.PEG)
    return not Tile.PEG in board.tiles[index+1:] and index



ENGLISH = Game(
    str_to_board("""\
  111
  111
1111111
1110111
1111111
  111
  111\
"""),
    lambda self, board: board == str_to_board("""\
  000
  000
0000000
0001000
0000000
  000
  000\
"""),
    18,
)

EUROPEAN = Game(
    str_to_board("""\
  111
 11111
1111111
1110111
1111111
 11111
  111\
"""),
    lambda self, board: board.width == self.board.width and last_peg(board),
    18,
)

DEBUG = Game(
    str_to_board("""\
11000
111111111
11100
00000
          11
          11\
"""),
    lambda self, board: board.tiles.count(Tile.PEG) < self.board.tiles.count(Tile.PEG),
    1,
)


CLEAR = "cls" if name == "nt" else "clear"

def clear():
    """Clears the screen"""
    system(CLEAR)

class CharacterAttribute:
    NORMAL = 0
    BOLD = 1
    RED = 91
    BLUE = 94

def character_attributes(*attributes):
    return f"\033[{';'.join(str(attribute) for attribute in attributes)}m"



class Element:
    NONE = " "
    HOLE = "o"
    PEG = "·"
    CURSOR = "*"

class Style:
    NORMAL = character_attributes(CharacterAttribute.NORMAL)
    CURSOR = character_attributes(CharacterAttribute.BOLD)
    CURSOR_SELECTED = character_attributes(CharacterAttribute.BOLD, CharacterAttribute.RED)
    JUMPED = character_attributes(CharacterAttribute.NORMAL, CharacterAttribute.RED)

def display(board, cursor, selected, jumped):
    clear()
    index = 0

    style = None
    def out(end):
        nonlocal style

        if index == cursor:
            if selected:
                newstyle = Style.CURSOR_SELECTED
            else:
                newstyle = Style.CURSOR
            element = Element.CURSOR
        elif index == jumped:
            newstyle = Style.JUMPED
            element = Element.HOLE
        else:
            newstyle = Style.NORMAL
            element = {
                None: Element.NONE,
                Tile.HOLE: Element.HOLE,
                Tile.PEG: Element.PEG,
            }[board.tiles[index]]

        if style != newstyle:
            style = newstyle
            print(style, end="")
        print(element, end=end)

    while index < len(board.tiles):
        end = index + board.width
        while index < end - 1:
            out(" ")
            index += 1
        out(None)
        index += 1



class DECMode:
    CURSOR = 25

def dec_mode_set(mode):
    return f"\033[?{mode}h"

def dec_mode_reset(mode):
    return f"\033[?{mode}l"



def cursor_show():
    print(dec_mode_set(DECMode.CURSOR), end="", flush=True)

def cursor_hide():
    print(dec_mode_reset(DECMode.CURSOR), end="", flush=True)



def index_right(list, element, start, end):
    return len(list) - 1 - list[::-1].index(element, len(list) - end, len(list) - start)



game = ENGLISH



atexit.register(cursor_show)

cursor_hide()



board = deepcopy(game.board)
moves = 0

cursor = board.tiles.index(Tile.PEG)
selected = False
jumped = None



cwd = getcwd()



while not game.won(game, board):
    display(board, cursor, selected, jumped)

    key = getkey()
    while not key in BINDS:
        key = getkey()

    action = BINDS[key]

    if action == Action.QUIT:
        clear()
        raise SystemExit
    elif action == Action.SAVE:
        cursor_show()
        print(cwd, end="/", flush=True)
        filename = input()
        cursor_hide()
        if filename != "":
            with open(filename, "bw") as file:
                Pickler(file).dump((board, moves))
    elif action == Action.LOAD:
        cursor_show()
        print(cwd, end="/", flush=True)
        filename = input()
        cursor_hide()
        if filename != "":
            with open(filename, "br") as file:
                (board, moves) = Unpickler(file).load()
    else:
        column_gin = cursor % board.width
        column_end = len(board.tiles) + column_gin
        row_gin = cursor - column_gin
        row_end = row_gin + board.width
        if selected:
            def jump(step, bound):
                global cursor, moves, jumped
                cmp = int.__lt__ if step >= 0 else int.__ge__
                if cmp(cursor + step * 2, bound) and board.tiles[cursor + step * 2] == Tile.HOLE and board.tiles[cursor + step] == Tile.PEG:
                    board.tiles[cursor] = Tile.HOLE
                    cursor += step
                    board.tiles[cursor] = Tile.HOLE
                    jumped = cursor
                    cursor += step
                    board.tiles[cursor] = Tile.PEG
                    moves += 1

            if action == Action.RIGHT:
                jump(1, row_end)
            elif action == Action.LEFT:
                jump(-1, row_gin)
            elif action == Action.DOWN:
                jump(board.width, len(board.tiles))
            elif action == Action.UP:
                jump(-board.width, 0)

            selected = False
        else:
            def move(step, gin, end, fall):
                def find(gin, end):
                    return gin + board.tiles[gin:end:step].index(Tile.PEG) * step

                try:
                    if cursor + step >= 0:
                        try:
                            return find(cursor + step, end)
                        except ValueError:
                            return find(gin, cursor) if gin != None else fall
                    else:
                        return find(gin, cursor) if gin != None else fall
                except ValueError:
                    return fall

            try:
                next = board.tiles.index(Tile.PEG, cursor + 1)
            except ValueError:
                next = board.tiles.index(Tile.PEG)

            try:
                previous = index_right(board.tiles, Tile.PEG, 0, cursor)
            except ValueError:
                previous = index_right(board.tiles, Tile.PEG, 0, len(board.tiles))

            if action == Action.RIGHT:
                cursor = move(1, None, row_end, next)
            elif action == Action.LEFT:
                cursor = move(-1, None, row_gin - 1 if row_gin - 1 >= 0 else None, previous)
            elif action == Action.DOWN:
                cursor = move(board.width, column_gin, column_end, next)
            elif action == Action.UP:
                cursor = move(-board.width, column_end - board.width, None, previous)
            else:
                selected = True



display(board, None, None, None)

if moves < game.minimum_moves:
    print("CHEATER")
elif moves == game.minimum_moves:
    print("NERD <3!")
else:
    print("GG!\nIn ", end="")
    print(moves, end="")
    print(" moves!")
