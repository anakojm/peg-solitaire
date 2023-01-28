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
Select "from" with the arrow keys or hjkl, confirm with enter or space
Cancel by reselecting "from" and confirming with enter or space
Select "to" with the arrow keys or hjkl, confirm with enter or space
TODO: Check for legal move
TODO: Save and resume
"""
from os import system, name
import sys
from getkey import getkey, keys

CHR_PEG = "·"
CHR_SELECTION = "\x1b[1m*\x1b[0m"  # bold
CHR_HOLE = "o"
CHR_FR = "\x1b[94m¤\x1b[0m"  # blue
CHR_TO = "\x1b[1m\x1b[91m*\x1b[0m"  # bold red
# TODO: implement a representation of the eaten peg
CHR_EATEN = "\x1b[91mo\x1b[0m"  # red
JUMP_LEFT = ["h", keys.LEFT]
JUMP_DOWN = ["j", keys.DOWN]
JUMP_UP = ["k", keys.UP]
JUMP_RIGHT = ["l", keys.RIGHT]
CONFIRM = [keys.ENTER, keys.SPACE]
QUIT = ["q", "m", keys.ESCAPE]
# See https://en.wikipedia.org/wiki/Peg_solitaire#Solutions_to_the_English_game
MIN_LEGAL_MOVES = 18

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
    print('\033[?25l', end="")  # hides the cursor
    for row in board:
        for col in row:
            print(col, end=" ")
        print("\n", end="")


def check_winned(set_number):
    """Checks the current position to see if the player won"""
    if overlay_board == win_position:
        if set_number < MIN_LEGAL_MOVES:
            print("CHEATER")
            sys.exit(1)
        elif set_number == MIN_LEGAL_MOVES:
            print("NERD <3!")
            sys.exit(0)
        else:
            print("GG!")
            print("In", set_number, "moves!")
            sys.exit(0)


def quit_game(set_number):
    clear()
    if set_number in [0, 1]:
        print("You quit after", set_number, "move.")
    else:
        print("You quit after", set_number, "moves.")
    sys.exit(0)


def main():
    # TODO: break down main function into smaller functions
    selection = (0, 0)
    to = (0, 0)
    old = " "
    set_number = 0
    confirm_fr = False
    confirm_to = False
    clear()
    while True:
        check_winned(set_number)

        while not confirm_fr:
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
                confirm_fr, confirm_to = True, False

            elif key in QUIT:
                quit_game(set_number)

            clear()

        if confirm_fr:
            board[selection[1]][selection[0]] = CHR_TO
            overlay_board[selection[1]][selection[0]] = CHR_FR
            old = CHR_FR
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

                elif key in CONFIRM and old in [CHR_FR, CHR_HOLE]:
                    if old == CHR_FR:
                        overlay_board[selection[1]][selection[0]] = CHR_PEG
                        board[selection[1]][selection[0]] = CHR_SELECTION
                        old = CHR_PEG
                        confirm_fr, confirm_to = False, False
                        clear()
                        # TODO: Don't use break to cancel
                        break
                    else:
                        confirm_to = True

                elif key in QUIT:
                    quit_game(set_number)
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
