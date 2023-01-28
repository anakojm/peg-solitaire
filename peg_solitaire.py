#!/bin/env python
"""
This is a game of peg solitaire in python
The goal of the game is to empty the board except for one center peg
To reach that goal you can move a piece, you can only move a piece by "jumping"
over another one, "eating" it in the process. The destination must be empty.
· indicates a peg in a hole, * emboldened indicates the peg to be moved,
and o indicates an empty hole. A blue ¤ is the hole the current peg moved from;
a red * is the final position of that peg,
a red o is the hole of the peg that was jumped and removed.
Select "from" with hjkl, confirm with enter
Select "to" with hjkl, confirm with enter
"""
from os import system, name
import sys
from getkey import getkey, keys

# jump_up, jump_down, jump_right, jump_left = False, False, False, False
CHR_PEG = "·"
CHR_SELECTION = "\x1b[1m*\x1b[0m"  # bold
CHR_HOLE = "o"
CHR_FR = "\x1b[94m¤\x1b[0m"  # blue
CHR_TO = "\x1b[1m\x1b[91m*\x1b[0m"  # bold red
# TODO: implement a representation of the eaten peg
CHR_EATEN = "\x1b[91mo\x1b[0m"  # red

overlay_board = [
    [" ", " ", CHR_PEG, CHR_PEG, CHR_PEG, " ", " "],
    [" ", " ", CHR_PEG, CHR_PEG, CHR_PEG, " ", " "],
    [CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG],
    [CHR_PEG, CHR_PEG, CHR_PEG, CHR_HOLE, CHR_PEG, CHR_PEG, CHR_PEG],
    [CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG],
    [" ", " ", CHR_PEG, CHR_PEG, CHR_PEG, " ", " "],
    [" ", " ", CHR_PEG, CHR_PEG, CHR_PEG, " ", " "],
]

board = [
    [CHR_SELECTION, " ", CHR_PEG, CHR_PEG, CHR_PEG, " ", " "],
    [" ", " ", CHR_PEG, CHR_PEG, CHR_PEG, " ", " "],
    [CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG],
    [CHR_PEG, CHR_PEG, CHR_PEG, CHR_HOLE, CHR_PEG, CHR_PEG, CHR_PEG],
    [CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG, CHR_PEG],
    [" ", " ", CHR_PEG, CHR_PEG, CHR_PEG, " ", " "],
    [" ", " ", CHR_PEG, CHR_PEG, CHR_PEG, " ", " "],
]

win_position = [
    [" ", " ", CHR_HOLE, CHR_HOLE, CHR_HOLE, " ", " "],
    [" ", " ", CHR_HOLE, CHR_HOLE, CHR_HOLE, " ", " "],
    [CHR_HOLE, CHR_HOLE, CHR_HOLE, CHR_HOLE, CHR_HOLE, CHR_HOLE, CHR_HOLE],
    [CHR_HOLE, CHR_HOLE, CHR_HOLE, CHR_PEG, CHR_HOLE, CHR_HOLE, CHR_HOLE],
    [CHR_HOLE, CHR_HOLE, CHR_HOLE, CHR_HOLE, CHR_HOLE, CHR_HOLE, CHR_HOLE],
    [" ", " ", CHR_HOLE, CHR_HOLE, CHR_HOLE, " ", " "],
    [" ", " ", CHR_HOLE, CHR_HOLE, CHR_HOLE, " ", " "],
]


def clear():
    """Clears the screen"""
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


def show_board():
    """Shows the board"""
    for i in board:
        for k in i:
            print(k, end=" ")
        print("\n", end="")


def main():
    # TODO: fix IndexError when going oob
    selection = (0, 0)
    to = (0, 0)
    old = " "
    set_number = 1
    confirm_fr = False
    confirm_to = False
    clear()
    while True:
        if overlay_board == win_position:
            if set_number < 18:
                print("CHEATER")
                sys.exit(1)
            elif set_number == 18:
                print("NERD <3!")
                sys.exit(0)
            else:
                print("GG!")
                print("In", set_number, "moves!")
                sys.exit(0)

        while not confirm_fr:
            show_board()
            key = getkey()
            if key == "h":
                board[selection[1]][selection[0]] = old
                old = overlay_board[selection[1]][selection[0] - 1]
                selection = selection[0] - 1, selection[1]
                board[selection[1]][selection[0]] = CHR_SELECTION

            elif key == "j":
                board[selection[1]][selection[0]] = old
                old = overlay_board[selection[1] + 1][selection[0]]
                selection = selection[0], selection[1] + 1
                board[selection[1]][selection[0]] = CHR_SELECTION

            elif key == "k":
                board[selection[1]][selection[0]] = old
                old = overlay_board[selection[1] - 1][selection[0]]
                selection = selection[0], selection[1] - 1
                board[selection[1]][selection[0]] = CHR_SELECTION

            elif key == "l":
                board[selection[1]][selection[0]] = old
                old = overlay_board[selection[1]][selection[0] + 1]
                selection = selection[0] + 1, selection[1]
                board[selection[1]][selection[0]] = CHR_SELECTION

            elif key == keys.ENTER and old == CHR_PEG:
                confirm_fr = True

            clear()

        if confirm_fr:
            board[selection[1]][selection[0]] = CHR_TO
            overlay_board[selection[1]][selection[0]] = CHR_FR
            old = CHR_FR
            to = selection
            while not confirm_to:
                show_board()
                key = getkey()
                if key == "h":
                    board[to[1]][to[0]] = old
                    old = overlay_board[to[1]][to[0] - 1]
                    to = to[0] - 1, to[1]
                    board[to[1]][to[0]] = CHR_TO

                elif key == "j":
                    board[to[1]][to[0]] = old
                    old = overlay_board[to[1] + 1][to[0]]
                    to = to[0], to[1] + 1
                    board[to[1]][to[0]] = CHR_TO

                elif key == "k":
                    board[to[1]][to[0]] = old
                    old = overlay_board[to[1] - 1][to[0]]
                    to = to[0], to[1] - 1
                    board[to[1]][to[0]] = CHR_TO

                elif key == "l":
                    board[to[1]][to[0]] = old
                    old = overlay_board[to[1]][to[0] + 1]
                    to = to[0] + 1, to[1]
                    board[to[1]][to[0]] = CHR_TO
                elif key == keys.ENTER and old in [CHR_FR, CHR_HOLE]:
                    # TODO: Fix redo move after cancel
                    if to == selection:
                        overlay_board[selection[1]][selection[0]] = CHR_PEG
                        board[selection[1]][selection[0]] = CHR_SELECTION
                        confirm_fr, confirm_to = False, False
                        old = CHR_PEG
                    confirm_to = True
                clear()

        if confirm_fr and confirm_to:
            board[(selection[1] + to[1]) // 2][(selection[0] + to[0]) // 2] = CHR_HOLE
            board[selection[1]][selection[0]] = CHR_HOLE
            board[to[1]][to[0]] = CHR_SELECTION
            overlay_board[(selection[1] + to[1]) // 2][
                (selection[0] + to[0]) // 2
            ] = CHR_HOLE
            overlay_board[selection[1]][selection[0]] = CHR_HOLE
            overlay_board[to[1]][to[0]] = CHR_PEG
            confirm_fr, confirm_to = False, False
            selection = to
            old = CHR_PEG
            set_number += 1


if __name__ == "__main__":
    main()
