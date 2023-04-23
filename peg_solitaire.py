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
import os
import sys
import ast
import atexit
from enum import IntEnum
from math import sqrt
from getkey import getkey, keys

# Settings:
EUROPEAN = False
ENGLISH = True
# EUROPEAN = True
# ENGLISH = False

# Keybinds
JUMP_LEFT = ["h", keys.LEFT]
JUMP_DOWN = ["j", keys.DOWN]
JUMP_UP = ["k", keys.UP]
JUMP_RIGHT = ["l", keys.RIGHT]
CONFIRM = [keys.ENTER, keys.SPACE]
QUIT = ["q", "m", keys.ESCAPE]
SAVE = ["s", "J"]
LOAD = ["L"]

class CharacterAttribute(IntEnum):
    NORMAL = 0
    BOLD = 1
    RED = 91
    BLUE = 94

def character_attributes(*attributes):
    return f"\033[{';'.join(str(int(attribute)) for attribute in attributes)}m"

# UI elements
CHR_EMPTY = " "
CHR_PEG = "·"
CHR_SELECTION = f"{character_attributes(CharacterAttribute.BOLD)}*{character_attributes(CharacterAttribute.NORMAL)}"
CHR_HOLE = "o"
CHR_FROM = f"{character_attributes(CharacterAttribute.BLUE)}¤{character_attributes(CharacterAttribute.NORMAL)}"
CHR_TO = f"{character_attributes(CharacterAttribute.BOLD, CharacterAttribute.RED)}*{character_attributes(CharacterAttribute.NORMAL)}"
CHR_EATEN = f"{character_attributes(CharacterAttribute.RED)}o{character_attributes(CharacterAttribute.NORMAL)}"

# See https://en.wikipedia.org/wiki/Peg_solitaire#Solutions_to_the_English_game
MIN_LEGAL_MOVES = 18
CAN_JUMP_OVER = [CHR_FROM, CHR_HOLE, CHR_EATEN]

def str_to_board(string):
    tiles = {
        " ": CHR_EMPTY,
        "0": CHR_HOLE,
        "1": CHR_PEG,
        "2": CHR_SELECTION,
    }
    return [[tiles[character] for character in line] for line in string.splitlines()]

# The code is flexible enough that you should be able to use any board
if ENGLISH:
    overlay_board = str_to_board(
"""\
  111  
  111  
1111111
1110111
1111111
  111  
  111  \
""")
    win_position = str_to_board(
"""\
  000  
  000  
0000000
0001000
0000000
  000  
  000  \
""")
# European version:
elif EUROPEAN:
    overlay_board = str_to_board(
"""\
  111  
 11111 
1111111
1110111
1111111
 11111 
  111  \
""")
    # No win_position, you win if there is one peg remaining

board = overlay_board
board[0][0] = CHR_SELECTION


class DECMode(IntEnum):
    CURSOR = 25


def dec_mode_set(mode):
    return f"\033[?{mode}h"


def dec_mode_reset(mode):
    return f"\033[?{mode}l"


def cursor_show():
    print(dec_mode_set(DECMode.CURSOR), end="", flush=True)


def cursor_hide():
    print(dec_mode_reset(DECMode.CURSOR), end="", flush=True)


def clear():
    """Clears the screen"""
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def show_board():
    """Shows the board"""
    clear()
    for row in board:
        for col in row:
            print(col, end=" ")
        print()


def check_winned():
    """Checks the current position to see if the player won"""
    if EUROPEAN:
        l_win = 0
        for row in overlay_board:
            for col in row:
                if col == CHR_PEG:
                    l_win += 1
        return l_win == 1
    elif ENGLISH:
        return overlay_board == win_position


def quit_game():
    """Function that is called upon pressing an element of the QUIT list"""
    clear()
    sys.exit(0)


def legal(selection, to):
    """
    Checks for legality of a move (if it is 0 or 3 stone long using the
    Pythagorean theorem, stay in school kids, it make you better at pvp).
    also checks if we are jumping over a peg or ourselves
    """
    return not (sqrt((selection[1] - to[1])**2 + (selection[0] - to[0])**2) not in [2, 0] or board[(selection[1] + to[1]) // 2][(selection[0] + to[0]) // 2] not in [CHR_PEG, CHR_TO])


def save(overlay_board):
    """
    Save the current game to a specified file
    TODO: fix load bug that lead to multiple CHR_EATEN by properly exporting
    all variables, don't forget to change CAN_JUMP_OVER after
    """
    cursor_show()
    print(os.getcwd(), end="")
    filename = input("/")
    if filename == "":
        return
    file = open(filename, "w")
    file.write(str(overlay_board))
    file.close()
    cursor_hide()


def load():
    """Load a game"""
    global CHR_SELECTION, board, overlay_board
    cursor_show()
    print(os.getcwd(), end="")
    filename = input("/")
    if filename == "":
        return
    file = open(filename, "r")
    overlay_board = file.read()
    file.close()
    board = overlay_board[:]
    board = ast.literal_eval(board)
    board[0][0] = CHR_SELECTION
    overlay_board = ast.literal_eval(overlay_board)
    cursor_hide()

atexit.register(cursor_show)

cursor_hide()

selection = (0, 0)
to = (0, 0)
old = " "
old_selection = selection
old_to = to
set_number = 0
confirm_from = False
confirm_to = False
# TODO: break down in smaller Functions
while True:
    if check_winned():
        clear()
        if set_number < MIN_LEGAL_MOVES:
            print("CHEATER")
        elif set_number == MIN_LEGAL_MOVES:
            print("NERD <3!")
        else:
            print(f"GG!\nIn {set_number} moves!")
        sys.exit(0)


    while not confirm_from:
        show_board()
        key = getkey()

        if key in JUMP_LEFT:
            board[selection[1]][selection[0]] = old
            old = overlay_board[selection[1]][(selection[0] - 1) % len(board)]
            selection = (selection[0] - 1) % len(board), selection[1]
            board[selection[1]][selection[0]] = CHR_SELECTION

        elif key in JUMP_DOWN:
            board[selection[1]][selection[0]] = old
            old = overlay_board[(selection[1] + 1) % len(board)][selection[0]]
            selection = selection[0], (selection[1] + 1) % len(board)
            board[selection[1]][selection[0]] = CHR_SELECTION

        elif key in JUMP_UP:
            board[selection[1]][selection[0]] = old
            old = overlay_board[(selection[1] - 1) % len(board)][selection[0]]
            selection = selection[0], (selection[1] - 1) % len(board)
            board[selection[1]][selection[0]] = CHR_SELECTION

        elif key in JUMP_RIGHT:
            board[selection[1]][selection[0]] = old
            old = overlay_board[selection[1]][(selection[0] + 1) % len(board)]
            selection = (selection[0] + 1) % len(board), selection[1]
            board[selection[1]][selection[0]] = CHR_SELECTION

        elif key in CONFIRM and old == CHR_PEG:
            confirm_from, confirm_to = True, False
            if set_number > 0:
                overlay_board[(old_selection[1] + old_to[1]) // 2][
                    (old_selection[0] + old_to[0]) // 2
                ] = CHR_HOLE
                board[(old_selection[1] + old_to[1]) // 2][(old_selection[0] + old_to[0]) // 2] = CHR_HOLE

        elif key in QUIT:
            quit_game()

        elif key in SAVE:
            save(overlay_board)

        elif key in LOAD:
            load()
            selection = (0, 0)
            to = (0, 0)
            old = " "
            old_selection = selection
            old_to = to
            set_number = 0
            confirm_from = False
            confirm_to = False

    board[selection[1]][selection[0]] = CHR_TO
    overlay_board[selection[1]][selection[0]] = CHR_FROM
    old = CHR_FROM
    to = selection
    while not confirm_to:
        show_board()
        key = getkey()

        if key in JUMP_LEFT:
            board[to[1]][to[0]] = old
            old = overlay_board[to[1]][(to[0] - 1) % len(board)]
            to = (to[0] - 1) % len(board), to[1]
            board[to[1]][to[0]] = CHR_TO

        elif key in JUMP_DOWN:
            board[to[1]][to[0]] = old
            old = overlay_board[(to[1] + 1) % len(board)][to[0]]
            to = to[0], (to[1] + 1) % len(board)
            board[to[1]][to[0]] = CHR_TO

        elif key in JUMP_UP:
            board[to[1]][to[0]] = old
            old = overlay_board[(to[1] - 1) % len(board)][to[0]]
            to = to[0], (to[1] - 1) % len(board)
            board[to[1]][to[0]] = CHR_TO

        elif key in JUMP_RIGHT:
            board[to[1]][to[0]] = old
            old = overlay_board[to[1]][(to[0] + 1) % len(board)]
            to = (to[0] + 1) % len(board), to[1]
            board[to[1]][to[0]] = CHR_TO

        elif key in CONFIRM and old in CAN_JUMP_OVER and legal(selection, to):
            if old == CHR_FROM:
                overlay_board[selection[1]][selection[0]] = CHR_PEG
                board[selection[1]][selection[0]] = CHR_SELECTION
                old = CHR_PEG
                confirm_from, confirm_to = False, False
                # TODO: Don't use break to cancel to selection
                break
            else:
                confirm_to = True

        elif key in QUIT:
            quit_game()

        # fixing CHR_EATEN issue would fix this too
        # elif key in SAVE:
        #     save(overlay_board)

        elif key in LOAD:
            load()
            selection = (0, 0)
            to = (0, 0)
            old = " "
            old_selection = selection
            old_to = to
            set_number = 0
            confirm_from = False
            confirm_to = False
            # TODO: Don't use break after load
            break

    if confirm_to:
        old_selection = selection
        old_to = to
        board[(selection[1] + to[1]) // 2][(selection[0] + to[0]) // 2] = CHR_EATEN
        board[selection[1]][selection[0]] = CHR_HOLE
        board[to[1]][to[0]] = CHR_SELECTION
        overlay_board[(selection[1] + to[1]) // 2][(selection[0] + to[0]) // 2] = CHR_EATEN
        overlay_board[selection[1]][selection[0]] = CHR_HOLE
        overlay_board[to[1]][to[0]] = CHR_PEG
        confirm_from = False
        confirm_to = False
        selection = to
        old = CHR_PEG
        set_number += 1
