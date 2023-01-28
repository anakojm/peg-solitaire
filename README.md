# Peg solitaire

A game of peg solitaire in the terminal, written in python

<br>

The goal of the game is to empty the board except for one center peg.

To reach that goal you can move a piece. You can only move a piece by "jumping"
over another one, "eating" it in the process. 

The destination must be empty.

<br>

- Select "from" with hjkl, confirm with enter
- Select "to" with hjkl, confirm with enter

<br>

UI: `·` indicates a peg in a hole, `*` emboldened indicates the peg to be moved,
and `o` indicates an empty hole. A blue `¤` is the hole the current peg moved from;
a red `*` is the final position of that peg.

Screenshot:

![UI showcase](https://gist.github.com/anakojm/f6ef6eba4160d95a59cfa3d500244051/raw/33848f36bfda2865ddaf2a5af69d1eac6794bfa6/showcase.png)

<br>

TODO: `grep -rnw peg_solitaire.py -e "TODO:"`
